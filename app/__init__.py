from quart import Quart
from quart_cors import cors
from quart_jwt_extended import JWTManager
from app.config import config_by_name
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.api.auth import auth_bp
from app.api.authors import authors_bp
from app.api.books import books_bp
from app.api.publishers import publishers_bp
from app.errors import errors_bp
from app.swagger import swagger_bp


def create_app(config_name="development"):
    app = Quart(__name__)
    app = cors(app, allow_origin="*")
    app.config.from_object(config_by_name[config_name])

    # Set up async SQLAlchemy engine and session
    db_url = app.config.get("SQLALCHEMY_DATABASE_URI")
    async_db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://")
    engine = create_async_engine(async_db_url, echo=True, future=True)
    session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # Attach to app context for use in repositories
    app.async_engine = engine
    app.async_session = session
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(authors_bp, url_prefix="/api/authors")
    app.register_blueprint(books_bp, url_prefix="/api/books")
    app.register_blueprint(publishers_bp, url_prefix="/api/publishers")
    app.register_blueprint(swagger_bp)

    # Initialize JWTManager
    JWTManager(app)

    @app.shell_context_processor
    def shell_context():
        return {"async_engine": engine, "async_session": session, "app": app}

    return app
