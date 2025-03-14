// Ініціалізація при завантаженні DOM
document.addEventListener('DOMContentLoaded', function() {
    // Ініціалізація Tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Анімація для лічильників на головній сторінці
    initCounterAnimation();

    // Підтвердження видалення
    initDeleteConfirmation();

    // Попередній перегляд завантажених зображень
    initImagePreview();

    // Анімація для кнопок під час надсилання форм
    initFormSubmitAnimation();

    // Валідація форм
    initFormValidation();
});

// Функція для анімації лічильників
function initCounterAnimation() {
    const counters = document.querySelectorAll('.counter');

    if (counters.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = parseInt(counter.innerHTML);
                    let count = 0;
                    const duration = 1500; // milliseconds
                    const step = target / (duration / 25);

                    const timer = setInterval(function() {
                        count += step;
                        counter.innerHTML = Math.floor(count);
                        if (count >= target) {
                            counter.innerHTML = target;
                            clearInterval(timer);
                        }
                    }, 25);

                    observer.unobserve(counter);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => {
            observer.observe(counter);
        });
    }
}

// Функція для підтвердження видалення
function initDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('.btn-delete-confirm');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Ви впевнені, що хочете видалити цей елемент? Ця дія не може бути скасована.')) {
                e.preventDefault();
            }
        });
    });
}

// Функція для попереднього перегляду завантажених зображень
function initImagePreview() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');

    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const previewContainer = document.getElementById(this.dataset.preview);

            if (previewContainer) {
                previewContainer.innerHTML = '';

                if (this.files.length > 0) {
                    previewContainer.parentElement.classList.remove('d-none');

                    for (let i = 0; i < this.files.length; i++) {
                        const file = this.files[i];

                        // Перевірка, чи файл є зображенням
                        if (!file.type.startsWith('image/')) continue;

                        const reader = new FileReader();
                        const imgContainer = document.createElement('div');
                        imgContainer.className = 'image-preview-item';

                        const img = document.createElement('img');
                        imgContainer.appendChild(img);
                        previewContainer.appendChild(imgContainer);

                        reader.onload = function(e) {
                            img.src = e.target.result;
                        };

                        reader.readAsDataURL(file);
                    }
                } else {
                    previewContainer.parentElement.classList.add('d-none');
                }
            }
        });
    });
}

// Функція для анімації кнопок під час надсилання форм
function initFormSubmitAnimation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');

            if (submitButton) {
                // Додаємо анімацію завантаження до кнопки
                submitButton.disabled = true;
                submitButton.classList.add('btn-loading');

                // Зберігаємо оригінальний текст кнопки
                const originalText = submitButton.textContent;
                submitButton.textContent = '';

                // Повертаємо оригінальний стан після завершення надсилання
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.classList.remove('btn-loading');
                    submitButton.textContent = originalText;
                }, 3000);
            }
        });
    });
}

// Функція для валідації форм на стороні клієнта
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');
        }, false);
    });
}

// Функція для попередперегляду завантажених зображень
function previewImage(input, preview) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// Функція для відкриття модального вікна з повноекранним переглядом зображення
function openImageModal(src) {
    const modal = new bootstrap.Modal(document.getElementById('imageModal'));
    document.getElementById('modalImage').src = src;
    modal.show();
}

// Функція для фільтрації завдань на сторінці списку завдань
function filterTasks() {
    const searchForm = document.getElementById('task-search-form');
    if (searchForm) {
        searchForm.submit();
    }
}

// Функція для очищення форми фільтрації
function clearFilters() {
    const form = document.getElementById('task-search-form');
    if (form) {
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.value = '';
        });
        form.submit();
    }
}

// Функція для зміни статусу завдання (AJAX)
function updateTaskStatus(taskId, status) {
    // Реалізація AJAX запиту для оновлення статусу завдання
    // Це псевдокод, який потрібно замінити реальною реалізацією
    fetch(`/tasks/${taskId}/status/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ status: status })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Оновлення UI після успішного оновлення статусу
            window.location.reload();
        } else {
            alert('Помилка при оновленні статусу завдання.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Виникла помилка при оновленні статусу завдання.');
    });
}

// Допоміжна функція для отримання CSRF-токена з cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}