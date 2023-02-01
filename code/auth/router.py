from fastapi import APIRouter

from code.auth import handlers

router = APIRouter()
router.add_api_route('/users', handlers.user_create_handler, methods=['post'])
router.add_api_route('/users', handlers.username_exists_handler)
router.add_api_route('/verify', handlers.verify_handler)
