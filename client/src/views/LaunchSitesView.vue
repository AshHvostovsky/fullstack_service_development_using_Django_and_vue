<script setup>
import { computed, ref, onBeforeMount, watch } from 'vue';
import axios from "axios"
import _ from 'lodash';
import {Modal} from 'bootstrap'

const launchsites = ref([])
const launchsiteToAdd = ref([])
const launchsiteToEdit = ref([])
const launchsiteToDelete = ref([]);

const launchsitesPictureRef = ref();
const launchsiteAddImageUrl = ref();
const newLaunchsitePicture = ref();
const showImageModalRef = ref();


const isSuperUser = ref(false);
const usersSites = ref([]);
const users = ref([]);


const loading = ref(false);

const stat_count = ref();
const stat_avg = ref();
const stat_max = ref();
const stat_min = ref();

const filterUser = ref(null);
const filterName = ref("");
const filterLocation = ref("");

function resetFilters() {
        filterName.value = "";
        filterLocation.value = "";

        // Перезапускаем запрос
        fetchLaunchSites();
};

watch(
    [filterName, filterLocation, filterUser],
    (newValues, oldValues) => {
        console.log("Фильтры изменились:", newValues); // Лог для проверки
        fetchLaunchSites();
    },
    { immediate: true } // Запуск при монтировании
);

async function fetchStats() {
    // Выполняем запрос для получения всех пользователей
    const response = await axios.get("/api/launchsites/stats"); // Запрос к вашему API
    stat_count.value = response.data.count
    stat_avg.value = response.data.avg
    stat_max.value = response.data.max
    stat_min.value = response.data.min
    console.log(stat_count)
}

const launchsiteById = computed(() => {
    return _.keyBy(launchsites.value, x => x.id)
})
const usersById = computed(() => {
    return _.keyBy(users.value, x => x.id)
})
async function fetchUserInfo() {
    const response = await axios.get("api/user-info/");
    console.log('User:', response.data.username);
    console.log('Email:', response.data.email);
    console.log('Superuser?:', response.data.is_superuser);
    isSuperUser.value = ref(response.data.is_superuser);
}
async function fetchUsersSites() {
    // Выполняем запрос для получения всех программ
    const r = await axios.get("/api/launchsites/", {
        params: {
            user_id: null, // Получаем все программы без фильтра по пользователю
        }
    });

    // Обновляем список программ (если это нужно)
    launchsites.value = r.data;

    // Используем Set для уникальных пользователей
    const usersSet = new Set();

    // Итерируем по каждой программе и добавляем уникальных пользователей в Set
    r.data.forEach(program => {
        if (program.user) {
            usersSet.add(program.user); // Добавляем пользователя, если он существует
        }
    });

    // Преобразуем Set в массив и записываем в ref переменную
    usersSites.value = Array.from(usersSet);

    // Для проверки выводим список пользователей в консоль
    console.log(usersSites.value);
}
async function fetchUsers() {
    // Выполняем запрос для получения всех пользователей
    const response = await axios.get("/api/users/"); // Запрос к вашему API
    users.value = response.data; // Сохраняем пользователей в переменной
    console.log(users.value)
}

async function launchsitesAddPictureChange() {
    launchsiteAddImageUrl.value = URL.createObjectURL(launchsitesPictureRef.value.files[0])
}

async function fetchLaunchSites() {
    loading.value = true;

    try {
        const r = await axios.get("/api/launchsites/", {
            params: {
                user_id: filterUser.value === "all" ? null : filterUser.value, // Фильтр по пользователю
                name: filterName.value || null, // Фильтр по названию
                location: filterLocation.value || null, // Фильтр по местоположению
            },
        });

        launchsites.value = r.data;
        console.log(r.data);
    } catch (error) {
        console.error("Ошибка при загрузке космодромов:", error);
    } finally {
        loading.value = false;
    }
}

async function onLaunchSiteAdd() {

    const formData = new FormData();

    formData.append('picture', launchsitesPictureRef.value.files[0]);

    formData.set('name', launchsiteToAdd.value.name)
    formData.set('location', launchsiteToAdd.value.location)

    await axios.post("/api/launchsites/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchLaunchSites();

    launchsiteToAdd.value.name = "";
    launchsiteToAdd.value.location = "";
    launchsiteAddImageUrl.value = "";
}
// async function onLaunchSiteAdd() {
//     await axios.post("/api/launchsites/", {
//         ...launchsiteToAdd.value,
//     });
//     await fetchLaunchSites();
// }
// async function onRemoveClick(launchsite) {
//     await axios.delete(`/api/launchsites/${launchsite.id}/`);
//     await fetchLaunchSites();
// }
async function onLaunchSiteEditClick(launchsite) {
    launchsiteToEdit.value = { ...launchsite };
}
async function onUpdateLaunchSite() {
    const formData = new FormData();

    // Добавляем данные о космическом аппарате
    formData.set('name', launchsiteToEdit.value.name);
    formData.set('location', launchsiteToEdit.value.location);

    // Если было выбрано новое изображение, добавляем его в запрос
    if (newLaunchsitePicture.value) {
        formData.append('picture', newLaunchsitePicture.value);
    }

    // Отправляем запрос
    await axios.put(`/api/launchsites/${launchsiteToEdit.value.id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });

    await fetchLaunchSites(); // обновляем данные
}
function onEditPictureChange(event) {
    newLaunchsitePicture.value = event.target.files[0]; // сохраняем выбранное изображение
}
onBeforeMount((async) => {
    fetchUserInfo()
    fetchUsers()
    fetchUsersSites()
    fetchLaunchSites(); //await
    fetchStats()
})


// Переменная для хранения выбранного изображения
const selectedImage = ref();

// Переменная для управления видимостью модального окна
const isImageModalVisible = ref(false);

// Функция для открытия модального окна с изображением
function openImageModal(imageUrl) {
    selectedImage.value = imageUrl;
    const modal = new Modal(showImageModalRef.value)
    modal.show();
}



async function onRemoveClick(launchsite) {
    await axios.delete(`/api/launchsites/${launchsite.id}/`);
    launchsiteToDelete.value = null;
    await fetchLaunchSites();
}
async function onLaunchSiteDeleteClick(launchsite) {
    launchsiteToDelete.value = { ...launchsite };
}
</script>

<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent.stop="onLaunchSiteAdd" class="p-4 shadow-sm rounded bg-light">
                <div class="row g-3">
                    <!-- Загрузка изображения -->
                    <div class="col-md-12">
                        <div class="d-flex align-items-center">
                            <!-- Поле выбора файла -->
                            <div class="me-3">
                                <input
                                    class="form-control"
                                    type="file"
                                    ref="launchsitesPictureRef"
                                    @change="launchsitesAddPictureChange"
                                />
                            </div>
                            <!-- Превью изображения -->
                            <div>
                                <img
                                    :src="launchsiteAddImageUrl"
                                    style="max-height: 60px;"
                                    alt=""
                                    class="img-thumbnail"
                                />
                            </div>
                        </div>
                    </div>
            
                    <!-- Название -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input
                                type="text"
                                id="launchsite_name"
                                class="form-control"
                                v-model="launchsiteToAdd.name"
                                required
                            />
                            <label for="launchsite_name">Название</label>
                        </div>
                    </div>
            
                    <!-- Местоположение -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input
                                type="text"
                                id="launchsite_location"
                                class="form-control"
                                v-model="launchsiteToAdd.location"
                                required
                            />
                            <label for="launchsite_location">Местоположение</label>
                        </div>
                    </div>
            
                    <!-- Кнопка добавления -->
                    <div class="col-12 text-end">
                        <button class="btn btn-primary">
                            <i class="bi bi-plus-circle"></i> Добавить космодром
                        </button>
                    </div>
                </div>
            </form>
            
            

            <div class="col-auto mt-4">
                <div v-if="isSuperUser.value == true">
                    <div class="form-floating filter">
                        <select name="user_id" id="user_id" class="form-select" v-model="filterUser">
                          <option value="all">Все</option>
                          <!-- Выводим список уникальных пользователей -->
                          <option :value="u" v-for="u in usersSites" :key="u">{{ usersById[u]?.username }}</option>
                        </select>
                        <label for="user_id">Фильтр по пользователю</label>
                      </div>

                      <!-- Статистика -->
                    <div class="stats-container row g-3">
                        <!-- Количество записей -->
                        <div class="col-md-12">
                            <div class="card shadow-sm h-100">
                                <div class="card-body text-center">
                                    <h5 class="card-title text-primary">
                                        <i class="bi bi-list-ol"></i> Количество записей
                                    </h5>
                                    <p class="card-text fs-4 fw-bold">{{ stat_count }}</p>
                                </div>
                            </div>
                        </div>

                    </div>
                    <div class="p-3 bg-light border rounded shadow-sm">
                        <h5 class="text-primary mb-3">
                            <i class="bi bi-funnel"></i> Фильтры
                        </h5>
                        <div class="row g-3">
                            <!-- Фильтр по названию -->
                            <div class="col-md-6">
                                <div class="form-floating">
                                    <input type="text" id="filter_name" class="form-control" v-model="filterName" placeholder="Название" />
                                    <label for="filter_name"><i class="bi bi-search"></i> Название</label>
                                </div>
                            </div>
                    
                            <!-- Фильтр по местоположению -->
                            <div class="col-md-6">
                                <div class="form-floating">
                                    <input type="text" id="filter_location" class="form-control" v-model="filterLocation" placeholder="Местоположение" />
                                    <label for="filter_location"><i class="bi bi-geo-alt"></i> Местоположение</label>
                                </div>
                            </div>
                    
                            <div class="row mt-3">
                                <div class="col text-end">
                                    <button class="btn btn-outline-secondary" @click="resetFilters">
                                        <i class="bi bi-arrow-counterclockwise"></i> Сбросить фильтры
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                
              </div>

              
                
            </div>

            <div v-if="loading">Гружу...</div>
            <div>
                <div v-for="item in launchsites" class="launchsite-item border p-3 mb-3">
                    <div class="row">
                        <!-- Название -->
                        <div class="col-12">
                            <strong>Название:</strong>
                            <div>{{ item.name }}</div>
                        </div>


                        <!-- Изображение -->
                        <div class="col-6 mb-3" v-if="item.picture">
                            <strong>Изображение:</strong>
                            <!-- Добавляем обработчик клика на изображение для открытия модального окна -->
                            <div>
                                <img :src="item.picture" alt="Изображение аппарата" style="max-height: 100px;" class="img-thumbnail" @click="openImageModal(item.picture)">
                            </div>
                        </div>


                        <!-- Местоположение -->
                        <div class="col-12">
                            <strong>Местоположение:</strong>
                            <div>{{ item.location }}</div>
                        </div>



                        <!-- Кнопки редактирования и удаления -->
                        <div class="col-12 mt-2 d-flex justify-content-start gap-2">
                            <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#editLaunchSiteModal"
                                @click="onLaunchSiteEditClick(item)">
                                <i class="bi bi-pencil"></i> Редактировать
                            </button>
                            <button class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteConfirmationModalRef"
                                @click="onLaunchSiteDeleteClick(item)">
                                <i class="bi bi-file-earmark-minus"></i> Удалить
                            </button>
                        </div>
                    </div>
                </div>
            </div>





            <!-- Modal -->
<div class="modal fade" id="editLaunchSiteModal" tabindex="-1" role="dialog"
aria-labelledby="exampleModalLabel" aria-hidden="true">
<div class="modal-dialog" role="document">
    <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Редактирование космодрома</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">

            <div class="row row-add">
                <!-- Название -->
                <div class="col">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="launchsiteToEdit.name" required>
                        <label for="floatingInput">Название</label>
                    </div>
                </div>

                <!-- Местоположение -->
                <div class="col">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="launchsiteToEdit.location" required>
                        <label for="floatingInput">Местоположение</label>
                    </div>
                </div>

                <!-- Текущее изображение -->
                <div class="col-12 text-center mb-3" v-if="launchsiteToEdit.picture">
                    <strong>Текущее изображение:</strong>
                    <div>
                        <img :src="launchsiteToEdit.picture" alt="Изображение космодрома" style="max-height: 150px;" class="img-thumbnail">
                    </div>
                </div>

                <!-- Поле для загрузки нового изображения -->
                <div class="col-12">
                    <label for="newPicture">Новое изображение</label>
                    <input type="file" class="form-control" id="newPicture" @change="onEditPictureChange">
                </div>
            </div>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                @click="onUpdateLaunchSite">Сохранить</button>
        </div>
    </div>
</div>
</div>





<div class="modal fade" ref="showImageModalRef" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content p-0">
            <!-- Кнопка закрытия справа сверху -->
            <button type="button" class="btn-close btn-close-right" data-bs-dismiss="modal"></button>

            <div class="modal-body p-0">
                <!-- Увеличенное изображение -->
                <img :src="selectedImage" alt="Увеличенное изображение" class="img-fluid img-modal">
            </div>
        </div>
    </div>
</div>


<!-- Modal для подтверждения удаления -->
<div class="modal fade" id="deleteConfirmationModalRef" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="deleteModalLabel">Подтверждение удаления</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                Вы уверены, что хотите удалить этот объект?
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="onRemoveClick(launchsiteToDelete)">Удалить</button>
            </div>
        </div>
    </div>
</div>


        </div>
    </div>
</template>

<style lang="scss" scoped>
.launchsite-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr auto auto auto;
    gap: 16px;
    align-items: center;
    align-content: center;
}
.row-add {
    padding: 0.5rem;
    margin: 0.5rem 0;
    display: flex;
    grid-template-columns: 1fr auto auto auto;
    gap: 16px;
    align-items: center;
    align-content: center;  
}

/* Общие стили для модального окна */
.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1050;
}

.modal-dialog {
    max-width: 600px;
    width: 100%;
}

.modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2);
    position: relative;
}

/* Стили для кнопки закрытия */
.btn-close-left {
    position: absolute;
    top: 10px;
    left: 10px;
    background: none;
    border: none;
    font-size: 1.5rem;
    color: #000;
}

.btn-close-left:hover {
    color: #f00;
    opacity: 0.8;
}

/* Стили для изображения */
.img-modal {
    max-height: 400px;
    object-fit: contain;
    border-radius: 10px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

/* Положение кнопок в подвале */
.modal-footer {
    padding-top: 20px;
}

.modal-footer .btn {
    padding: 10px 20px;
}



/* Стили для модального окна с изображением */
.modal-content.p-0 {
    border: none;
    background-color: transparent;
    box-shadow: none;
    padding: 0;
    max-width: fit-content; /* Окно адаптируется к размеру изображения */
    position: relative;
}

.btn-close-right {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 1051;
    background-color: red;
    opacity: 1;
}

.btn-close-right:hover {
    background-color: darkred;
}

.img-modal {
    display: block;
    max-width: 100%;
    height: auto;
}
.filter {
    padding: 0.1rem;
}
.stats-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
    background-color: #ffffff;
    border-radius: 8px;
    
}

.stat-item {
    margin: 0 10px;
    font-size: 1.1rem;
    color: #2c0727;
}

.stat-item strong {
    color: #461574;
}
</style>
