import os
import sys
import argparse
from src import create_app
from src.extensions import get_session
from src.models.respuesta import Respuesta


def is_safe_to_run(app, allow_env_var='ALLOW_DB_CLEAN'):
    # Allow if app is in testing mode
    if app.config.get('TESTING'):
        return True, 'app.config["TESTING"] is True'

    # Allow if explicit env var is set
    if os.environ.get(allow_env_var) == '1':
        return True, f'environment variable {allow_env_var}=1'

    # Otherwise deny by default
    return False, 'neither TESTING nor env var set'


def main():
    parser = argparse.ArgumentParser(description='Clear test responses for a user (safe guard enabled)')
    parser.add_argument('--user-id', type=int, default=1, help='User id whose respuestas will be deleted (default: 1)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without performing deletion')
    parser.add_argument('--force', action='store_true', help='Force deletion even if environment checks fail')
    args = parser.parse_args()

    app = create_app()
    session = get_session()

    safe, reason = is_safe_to_run(app)
    if not safe and not args.force:
        print('ERROR: Aborting. Unsafe to run clean script against this environment.')
        print('Reason:', reason)
        print('To override, set environment variable ALLOW_DB_CLEAN=1 or pass --force (use with extreme caution).')
        sys.exit(2)

    # Additional safety: if DB URI looks like production, warn and abort unless forced
    db_uri = (
        f"mysql+pymysql://{app.config.get('MYSQL_USER')}:"
        f"{app.config.get('MYSQL_PASSWORD')}@"
        f"{app.config.get('MYSQL_HOST')}/{app.config.get('MYSQL_DB')}"
    )
    prod_indicators = ['prod', 'amazonaws', 'rds', 'azure', 'cloud']
    allow_env = os.environ.get('ALLOW_DB_CLEAN') == '1'
    if any(ind in db_uri.lower() for ind in prod_indicators) and not args.force and not app.config.get('TESTING') and not allow_env:
        print('ERROR: Detected a database URI that may be production-like:', db_uri)
        print('Refusing to run without --force or ALLOW_DB_CLEAN=1. Set --dry-run to inspect what would be deleted.')
        sys.exit(3)

    user_id = args.user_id
    count = session.query(Respuesta).filter(Respuesta.id_usuario == user_id).count()
    print(f'Found {count} respuestas for user {user_id}.')
    if args.dry_run:
        print('Dry run enabled — no changes made.')
        return

    deleted = session.query(Respuesta).filter(Respuesta.id_usuario == user_id).delete()
    session.commit()
    print(f'Deleted {deleted} respuestas for user {user_id}')


if __name__ == '__main__':
    main()
