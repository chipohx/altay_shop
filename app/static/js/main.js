document.addEventListener('DOMContentLoaded', function() {
    // Handle search form in header
    const headerSearchForm = document.querySelector('.search-form-compact');
    if (headerSearchForm) {
        headerSearchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchInput = this.querySelector('input');
            const searchTerm = searchInput.value.trim();
            if (searchTerm) {
                searchProducts(searchTerm);
                // Перенаправляем на главную страницу, если мы не на ней
                if (window.location.pathname !== '/') {
                    window.location.href = `/?search=${encodeURIComponent(searchTerm)}`;
                    return;
                }
            }
        });
    }

    // Check for product detail page and product data 
    const productDetailElement = document.getElementById('product-detail');
    if (productDetailElement) {
        // Check if we need to load product data via API
        if (productDetailElement.querySelector('.loading')) {
            const productId = productDetailElement.dataset.productId;
            fetchProductData(productId);
        }
    }

    // Homepage - fetch featured products and regular products
    const featuredProducts = document.getElementById('featured-products');
    if (featuredProducts) {
        fetchFeaturedProducts();
    }
    
    // Homepage - fetch all products for recommendations
    const productGrid = document.getElementById('product-grid');
    if (productGrid) {
        fetchAllProducts();
    }

    // Categories page - fetch all categories
    const categoryList = document.getElementById('category-list');
    if (categoryList) {
        fetchAllCategories();
    }

    // Check for search parameters in URL
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('search');
    if (searchQuery) {
        searchProducts(searchQuery);
        
        // Update the search input
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.value = searchQuery;
        }
    }
    
    // Check for category filter in URL
    const categoryId = urlParams.get('category');
    if (categoryId) {
        fetchProductsByCategory(categoryId);
    }
});

// Fetch featured products (top 4 products for showcase)
async function fetchFeaturedProducts() {
    try {
        const response = await fetch('/api/v1/products');
        if (!response.ok) {
            throw new Error('Failed to fetch featured products');
        }
        const products = await response.json();
        
        // Для демонстрации: берем первые 4 товара как "лучшие"
        // В реальном проекте здесь может быть отдельный API-эндпоинт для лучших товаров
        const featuredProducts = products.slice(0, 4);
        renderFeaturedProducts(featuredProducts);
    } catch (error) {
        console.error('Error fetching featured products:', error);
        showErrorMessage('Не удалось загрузить лучшие товары');
    }
}

// Fetch products by category
async function fetchProductsByCategory(categoryId) {
    try {
        // В идеале здесь должен быть API эндпоинт для фильтрации по категории
        // Но для демонстрации используем клиентскую фильтрацию
        const response = await fetch('/api/v1/products');
        if (!response.ok) {
            throw new Error('Failed to fetch products');
        }
        const allProducts = await response.json();
        const filteredProducts = allProducts.filter(product => product.category_id == categoryId);
        
        renderProductGrid(filteredProducts);
        
        // Обновляем заголовок секции
        const sectionTitle = document.querySelector('.recommendations-section h2');
        if (sectionTitle) {
            sectionTitle.textContent = 'Товары выбранной категории';
        }
    } catch (error) {
        console.error('Error fetching products by category:', error);
        showErrorMessage('Не удалось загрузить товары категории');
    }
}

// Render featured products
function renderFeaturedProducts(products) {
    const featuredProductsContainer = document.getElementById('featured-products');
    if (!featuredProductsContainer) return;
    
    // Clear existing content
    featuredProductsContainer.innerHTML = '';
    
    if (products.length === 0) {
        featuredProductsContainer.innerHTML = '<p class="no-results">Лучшие товары не найдены</p>';
        return;
    }
    
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'featured-product-card';
        
        // Use the main photo if available, otherwise use a placeholder
        const imageUrl = product.main_photo 
            ? product.main_photo 
            : '/static/image/placeholder.jpg';
        
        productCard.innerHTML = `
            <div class="featured-product-image">
                <img src="${imageUrl}" alt="${product.title}">
            </div>
            <div class="featured-product-info">
                <h3 class="featured-product-title">${product.title}</h3>
                <p class="featured-product-price">${product.price.toFixed(2)} ₽</p>
                <a href="/product/${product.id}" class="btn">Подробнее</a>
            </div>
        `;
        
        featuredProductsContainer.appendChild(productCard);
    });
}

// Fetch a single product by ID
async function fetchProductData(productId) {
    try {
        const response = await fetch(`/api/v1/products/${productId}`);
        if (!response.ok) {
            throw new Error('Product not found');
        }
        const product = await response.json();
        renderProductDetail(product);
    } catch (error) {
        console.error('Error fetching product:', error);
        showErrorMessage('Не удалось загрузить данные о товаре');
    }
}

// Fetch all products
async function fetchAllProducts() {
    try {
        const response = await fetch('/api/v1/products');
        if (!response.ok) {
            throw new Error('Failed to fetch products');
        }
        const products = await response.json();
        renderProductGrid(products);
    } catch (error) {
        console.error('Error fetching products:', error);
        showErrorMessage('Не удалось загрузить товары');
    }
}

// Search products
async function searchProducts(searchTerm) {
    try {
        const response = await fetch(`/api/v1/products/search?q=${encodeURIComponent(searchTerm)}`);
        if (!response.ok) {
            throw new Error('Search failed');
        }
        const products = await response.json();
        renderProductGrid(products);
        
        // Update search results message
        const searchResults = document.getElementById('search-results');
        if (searchResults) {
            searchResults.textContent = `Результаты поиска: ${products.length} найдено`;
        }
        
        // Обновляем заголовок секции
        const sectionTitle = document.querySelector('.recommendations-section h2');
        if (sectionTitle) {
            sectionTitle.textContent = `Результаты поиска для "${searchTerm}"`;
        }
    } catch (error) {
        console.error('Error searching products:', error);
        showErrorMessage('Ошибка при поиске товаров');
    }
}

// Fetch all categories
async function fetchAllCategories() {
    try {
        const response = await fetch('/api/v1/categories');
        if (!response.ok) {
            throw new Error('Failed to fetch categories');
        }
        const categories = await response.json();
        renderCategoryList(categories);
    } catch (error) {
        console.error('Error fetching categories:', error);
        showErrorMessage('Не удалось загрузить категории');
    }
}

// Render product grid on homepage
function renderProductGrid(products) {
    const productGrid = document.getElementById('product-grid');
    if (!productGrid) return;
    
    // Clear existing content
    productGrid.innerHTML = '';
    
    if (products.length === 0) {
        productGrid.innerHTML = '<p class="no-results">Товары не найдены</p>';
        return;
    }
    
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        
        // Use the main photo if available, otherwise use a placeholder
        const imageUrl = product.main_photo 
            ? product.main_photo 
            : '/static/image/placeholder.jpg';
        
        productCard.innerHTML = `
            <div class="product-image">
                <img src="${imageUrl}" alt="${product.title}">
            </div>
            <div class="product-info">
                <h3 class="product-title">${product.title}</h3>
                <p class="product-description">${product.description.substring(0, 100)}${product.description.length > 100 ? '...' : ''}</p>
                <p class="product-price">${product.price.toFixed(2)} ₽</p>
                <a href="/product/${product.id}" class="btn">Подробнее</a>
            </div>
        `;
        
        productGrid.appendChild(productCard);
    });
}

// Render product detail page
function renderProductDetail(product) {
    const productDetail = document.getElementById('product-detail');
    if (!productDetail) return;
    
    // Use the main photo if available, otherwise use a placeholder
    const mainImageUrl = product.main_photo 
        ? product.main_photo 
        : '/static/image/placeholder.jpg';
    
    // Create an array of all photos with the main photo first
    const allPhotos = [];
    if (product.main_photo) {
        allPhotos.push(product.main_photo);
    }
    if (product.additional_photos && product.additional_photos.length > 0) {
        allPhotos.push(...product.additional_photos);
    }
    
    // Prepare slider HTML if there are photos
    let sliderHTML = '';
    if (allPhotos.length > 0) {
        sliderHTML = `
            <div class="additional-photos-container">
                <h3>Все фотографии</h3>
                <div class="slider-container">
                    <button class="slider-arrow prev-arrow" onclick="moveSlider(-1)">&#10094;</button>
                    <div class="additional-photos-slider">
                        <div class="slider-track" id="slider-track">
                            ${allPhotos.map((photo, index) => `
                                <div class="additional-photo">
                                    <img src="${photo}" alt="${product.title} - Фото ${index + 1}" 
                                        onclick="setMainImage('${photo}')">
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    <button class="slider-arrow next-arrow" onclick="moveSlider(1)">&#10095;</button>
                </div>
            </div>
        `;
    }
    
    const detailContent = `
        <div class="product-gallery">
            <div class="main-photo">
                <img src="${mainImageUrl}" alt="${product.title}" id="main-product-image">
            </div>
        </div>
        <div class="product-detail-info">
            <h1>${product.title}</h1>
            <p class="product-detail-price">${product.price.toFixed(2)} ₽</p>
            <div class="product-detail-description">
                ${product.description}
            </div>
            <a href="/" class="btn btn-secondary">Назад к товарам</a>
            ${sliderHTML}
        </div>
    `;
    
    productDetail.innerHTML = detailContent;
    
    // Initialize slider variables and functions
    if (allPhotos.length > 0) {
        window.sliderPosition = 0;
        
        window.setMainImage = function(imageSrc) {
            const mainImage = document.getElementById('main-product-image');
            if (mainImage) {
                mainImage.src = imageSrc;
                
                // Update active state of thumbnails
                const thumbnails = document.querySelectorAll('.additional-photo img');
                thumbnails.forEach(thumb => {
                    const thumbParent = thumb.parentElement;
                    if (thumb.src === imageSrc) {
                        thumbParent.classList.add('active');
                    } else {
                        thumbParent.classList.remove('active');
                    }
                });
            }
        };
        
        window.moveSlider = function(direction) {
            const photoCount = allPhotos.length;
            const visiblePhotos = window.innerWidth < 768 ? 2 : 3; // Show fewer on mobile
            const maxPosition = Math.max(0, photoCount - visiblePhotos);
            
            window.sliderPosition += direction;
            
            // Clamp position between 0 and maxPosition
            if (window.sliderPosition < 0) window.sliderPosition = 0;
            if (window.sliderPosition > maxPosition) window.sliderPosition = maxPosition;
            
            // Move the slider
            const sliderTrack = document.getElementById('slider-track');
            if (sliderTrack) {
                sliderTrack.style.transform = `translateX(-${window.sliderPosition * 33.33}%)`;
            }
        };
    }
}

// Render category list
function renderCategoryList(categories) {
    const categoryList = document.getElementById('category-list');
    if (!categoryList) return;
    
    // Clear existing content
    categoryList.innerHTML = '';
    
    if (categories.length === 0) {
        categoryList.innerHTML = '<p class="no-results">Категории не найдены</p>';
        return;
    }
    
    categories.forEach(category => {
        const categoryCard = document.createElement('div');
        categoryCard.className = 'category-card';
        
        categoryCard.innerHTML = `
            <h3 class="category-name">${category.name}</h3>
        `;
        
        categoryCard.addEventListener('click', () => {
            window.location.href = `/?category=${category.id}`;
        });
        
        categoryList.appendChild(categoryCard);
    });
}

// Show error message
function showErrorMessage(message) {
    const errorContainer = document.createElement('div');
    errorContainer.className = 'error-message';
    errorContainer.textContent = message;
    
    // Add to DOM
    document.querySelector('main .container').prepend(errorContainer);
    
    // Remove after 5 seconds
    setTimeout(() => {
        errorContainer.remove();
    }, 5000);
} 