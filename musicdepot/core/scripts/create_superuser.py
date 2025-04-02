from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin@example.com").exists():
    User.objects.create_superuser(
        username="admin@example.com",
        email="admin@example.com",
        password="securepassword123"
    )
    print("✅ Superuser created.")
else:
    print("✅ Superuser already exists.")
