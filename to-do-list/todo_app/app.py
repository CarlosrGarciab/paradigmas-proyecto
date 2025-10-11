from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import os
from models import db, Task

app = Flask(__name__)

# Configuración de la aplicación
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu-clave-secreta-super-segura')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///todo_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

@app.context_processor
def inject_now():
    """Inyectar la fecha actual en todos los templates."""
    return {'now': datetime.now()}

@app.before_request
def create_tables():
    """Crear las tablas de la base de datos si no existen."""
    if not hasattr(app, '_database_initialized'):
        with app.app_context():
            db.create_all()
        app._database_initialized = True

@app.route('/')
def index():
    """
    Página principal que muestra todas las tareas.
    """
    # Obtener parámetros de filtro y ordenación
    filter_status = request.args.get('status', 'all')
    sort_by = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    
    # Construir la consulta base
    query = Task.query
    
    # Aplicar filtros
    if filter_status == 'completed':
        query = query.filter(Task.completed == True)
    elif filter_status == 'pending':
        query = query.filter(Task.completed == False)
    
    # Aplicar ordenación
    if hasattr(Task, sort_by):
        if order == 'desc':
            query = query.order_by(getattr(Task, sort_by).desc())
        else:
            query = query.order_by(getattr(Task, sort_by))
    
    tasks = query.all()
    
    # Estadísticas
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter(Task.completed == True).count()
    pending_tasks = total_tasks - completed_tasks
    
    stats = {
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': pending_tasks,
        'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
    }
    
    return render_template('index.html', 
                         tasks=tasks, 
                         stats=stats,
                         current_filter=filter_status,
                         current_sort=sort_by,
                         current_order=order)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    """
    Página para agregar una nueva tarea.
    """
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'medium')
        due_date_str = request.form.get('due_date', '')
        
        # Validaciones
        if not title:
            flash('El título de la tarea es obligatorio.', 'error')
            return render_template('add_task.html')
        
        # Procesar fecha de vencimiento
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de fecha inválido.', 'error')
                return render_template('add_task.html')
        
        # Crear nueva tarea
        new_task = Task(
            title=title,
            description=description if description else None,
            priority=priority,
            due_date=due_date
        )
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al agregar la tarea.', 'error')
            app.logger.error(f'Error al agregar tarea: {e}')
    
    return render_template('add_task.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """
    Página para editar una tarea existente.
    """
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'medium')
        due_date_str = request.form.get('due_date', '')
        completed = request.form.get('completed') == 'on'
        
        # Validaciones
        if not title:
            flash('El título de la tarea es obligatorio.', 'error')
            return render_template('edit_task.html', task=task)
        
        # Procesar fecha de vencimiento
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de fecha inválido.', 'error')
                return render_template('edit_task.html', task=task)
        
        # Actualizar tarea
        task.title = title
        task.description = description if description else None
        task.priority = priority
        task.due_date = due_date
        task.completed = completed
        task.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar la tarea.', 'error')
            app.logger.error(f'Error al actualizar tarea: {e}')
    
    return render_template('edit_task.html', task=task)

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    """
    Cambiar el estado de completado de una tarea (AJAX).
    """
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'completed': task.completed,
            'message': 'Tarea actualizada exitosamente.'
        })
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error al cambiar estado de tarea: {e}')
        return jsonify({
            'success': False,
            'message': 'Error al actualizar la tarea.'
        }), 500

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """
    Eliminar una tarea.
    """
    task = Task.query.get_or_404(task_id)
    success = True
    error_message = None
    try:
        db.session.delete(task)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        success = False
        error_message = str(e)
        flash('Error al eliminar la tarea.', 'error')
        app.logger.error(f'Error al eliminar tarea: {e}')

    # Si la solicitud es AJAX/fetch, devolver JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json or request.accept_mimetypes['application/json']:
        return jsonify({'success': success, 'error': error_message})
    # Si es formulario normal, redirigir
    return redirect(url_for('index'))

@app.route('/api/tasks')
def api_tasks():
    """
    API endpoint para obtener todas las tareas en formato JSON.
    """
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/stats')
def api_stats():
    """
    API endpoint para obtener estadísticas de las tareas.
    """
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter(Task.completed == True).count()
    pending_tasks = total_tasks - completed_tasks
    
    # Estadísticas por prioridad
    priority_stats = {}
    for priority in ['low', 'medium', 'high']:
        priority_stats[priority] = Task.query.filter(Task.priority == priority).count()
    
    return jsonify({
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': pending_tasks,
        'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1),
        'priority_stats': priority_stats
    })

@app.errorhandler(404)
def not_found_error(error):
    """Manejador de error 404."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejador de error 500."""
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)