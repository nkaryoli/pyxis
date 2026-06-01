import argparse
import sys
from src import create_app
from src.extensions import get_session
from src.models.usuario import Usuario


def main():
    parser = argparse.ArgumentParser(description='Reactivate a user by id (sets is_active=True)')
    parser.add_argument('--user-id', type=int, default=1, help='ID of the user to reactivate (default: 1)')
    args = parser.parse_args()

    app = create_app()
    session = get_session()

    try:
        usuario = session.query(Usuario).filter(Usuario.id_usuario == args.user_id).first()
        if not usuario:
            print(f'No user found with id {args.user_id}')
            sys.exit(1)
        usuario.is_active = True
        session.commit()
        print(f'User {args.user_id} reactivated (is_active=True)')
    except Exception as e:
        session.rollback()
        print('Error:', e)
        sys.exit(2)
    finally:
        session.close()


if __name__ == '__main__':
    main()
