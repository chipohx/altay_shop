document.addEventListener('DOMContentLoaded', function() {
    // Обработка удаления элементов с подтверждением
    const deleteLinks = document.querySelectorAll('.delete-link');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить этот элемент?')) {
                e.preventDefault();
            }
        });
    });
    
    // Обработка загрузки главного изображения
    const mainPhotoInput = document.getElementById('main_photo');
    if (mainPhotoInput) {
        mainPhotoInput.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                const file = this.files[0];
                if (!file.type.startsWith('image/')) return;
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Найдем ближайший .image-preview контейнер к этому input
                    const previewContainer = mainPhotoInput.closest('.form-group').querySelector('.image-preview');
                    if (previewContainer) {
                        previewContainer.innerHTML = '';
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.alt = 'Главное фото';
                        previewContainer.appendChild(img);
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Обработка загрузки дополнительных изображений
    const additionalPhotosInput = document.getElementById('additional_photos');
    if (additionalPhotosInput) {
        additionalPhotosInput.addEventListener('change', function() {
            const previewContainer = document.getElementById('image-preview');
            if (!previewContainer) return;
            
            previewContainer.innerHTML = '';
            
            if (this.files && this.files.length > 0) {
                for (let i = 0; i < this.files.length; i++) {
                    const file = this.files[i];
                    if (!file.type.startsWith('image/')) continue;
                    
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.alt = file.name;
                        previewContainer.appendChild(img);
                    };
                    reader.readAsDataURL(file);
                }
            }
        });
    }
    
    // Обработка формы товара
    const productForm = document.getElementById('product-form');
    if (productForm) {
        productForm.addEventListener('submit', function(e) {
            const titleInput = document.getElementById('title');
            const priceInput = document.getElementById('price');
            const categoryInput = document.getElementById('category_id');
            const descriptionInput = document.getElementById('description');
            
            // Простая валидация
            if (!titleInput.value.trim()) {
                e.preventDefault();
                alert('Пожалуйста, введите название товара');
                return;
            }
            
            if (!priceInput.value || parseFloat(priceInput.value) <= 0) {
                e.preventDefault();
                alert('Пожалуйста, введите корректную цену');
                return;
            }
            
            if (!categoryInput.value) {
                e.preventDefault();
                alert('Пожалуйста, выберите категорию');
                return;
            }
            
            if (!descriptionInput.value.trim()) {
                e.preventDefault();
                alert('Пожалуйста, введите описание товара');
                return;
            }
        });
    }
    
    // Обработка формы категории
    const categoryForm = document.getElementById('category-form');
    if (categoryForm) {
        categoryForm.addEventListener('submit', function(e) {
            const nameInput = document.getElementById('category-name');
            if (!nameInput.value.trim()) {
                e.preventDefault();
                alert('Пожалуйста, введите название категории');
                return;
            }
        });
    }
}); 