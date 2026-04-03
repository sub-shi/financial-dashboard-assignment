from flask import Flask
from config import Config
from database import db

# Import models (IMPORTANT: needed before create_all)
from models.user import User
from models.role import Role
from models.record import Record

# Import routes
from routes.auth_routes import auth_bp
from routes.record_routes import record_bp
from routes.dashboard_routes import dashboard_bp
from routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    #SEED FUNCTIONS FOR ROLES AND USERS
    def seed_roles():
        roles = ["viewer", "analyst", "admin"]
        for r in roles:
            if not Role.query.filter_by(name=r).first():
                db.session.add(Role(name=r))
        db.session.commit()

    def seed_users():
        admin_role = Role.query.filter_by(name="admin").first()

        if admin_role and not User.query.filter_by(email="admin@example.com").first():
            user = User(
                name="Admin",
                email="admin@example.com",
                role_id=admin_role.id
            )
            db.session.add(user)
            db.session.commit()

    #INIT DB
    with app.app_context():
        db.create_all()
        seed_roles()
        seed_users()

    #ROUTES
    @app.route("/")
    def home():
        return {"message": "Finance Backend Running"}

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(record_bp, url_prefix="/records")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(user_bp, url_prefix="/users")
    return app


# Create app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)