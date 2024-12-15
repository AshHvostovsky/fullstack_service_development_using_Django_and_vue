<script setup>
import { computed, ref, onBeforeMount, watch } from 'vue';
import axios from "axios"
import _ from 'lodash';
import {Modal} from 'bootstrap'


const spacecrafts = ref([]);
const missions = ref([]);
const launchsites = ref([]);

const spacecraftToAdd = ref([]);
const spacecraftToEdit = ref([]);
const spacecraftToDelete = ref([]);

const spacecraftsPictureRef = ref();
const spacecraftAddImageUrl = ref();
const newSpacecraftPicture = ref();
const showImageModalRef = ref();

const isSuperUser = ref(false);
const usersSpaceCrafts = ref([]);
const users = ref([]);

const loading = ref(false);

const stat_count = ref();
const stat_avg = ref();
const stat_max = ref();
const stat_min = ref();
const stat_pop_man = ref();

const is2FAEnabled = ref(false);


const filterUser = ref(null);
const filterName = ref("");
const filterManufacturer = ref("");
const filterLaunchSite = ref(null);
const filterMission = ref(null);

function resetFilters() {
        filterName.value = "";
        filterManufacturer.value = null;
        filterLaunchSite.value = "";
        filterMission.value = "";

        // Перезапускаем запрос миссий
        fetchSpaceCrafts();
};

watch(
    [filterName, filterManufacturer, filterLaunchSite, filterMission, filterUser],
    (newValues, oldValues) => {
        console.log("Фильтры изменились:", newValues); // Лог для проверки
        fetchSpaceCrafts();
    },
    { immediate: true } // Запуск при монтировании
);

async function fetchStats() {
    // Выполняем запрос для получения всех пользователей
    const response = await axios.get("/api/spacecrafts/stats"); // Запрос к вашему API
    stat_count.value = response.data.count
    stat_avg.value = response.data.avg
    stat_max.value = response.data.max
    stat_min.value = response.data.min
    stat_pop_man.value = response.data.most_popular_manufacturer
    console.log(stat_count)
}

const spacecraftsById = computed(() => {
    return _.keyBy(spacecrafts.value, x => x.id)
})
const missionsById = computed(() => {
    return _.keyBy(missions.value, x => x.id)
})
const launchsitesById = computed(() => {
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
        is2FAEnabled.value = ref(response.data.is_2fa_enabled); // Сохранение информации о 2FA
    }
    async function fetchUsersSpaceCrafts() {
        // Выполняем запрос для получения всех программ
        const r = await axios.get("/api/spacecrafts/", {
            params: {
                user_id: null, // Получаем все программы без фильтра по пользователю
            }
        });

        // Обновляем список программ (если это нужно)
        spacecrafts.value = r.data;

        // Используем Set для уникальных пользователей
        const usersSet = new Set();

        // Итерируем по каждой программе и добавляем уникальных пользователей в Set
        r.data.forEach(spacecraft => {
            if (spacecraft.user) {
                usersSet.add(spacecraft.user); // Добавляем пользователя, если он существует
            }
        });

        // Преобразуем Set в массив и записываем в ref переменную
        usersSpaceCrafts.value = Array.from(usersSet);

        // Для проверки выводим список пользователей в консоль
        console.log(usersSpaceCrafts.value);
    }
    async function fetchUsers() {
        // Выполняем запрос для получения всех пользователей
        const response = await axios.get("/api/users/"); // Запрос к вашему API
        users.value = response.data; // Сохраняем пользователей в переменной
        console.log(users.value)
    }


async function spacecraftsAddPictureChange() {
    spacecraftAddImageUrl.value = URL.createObjectURL(spacecraftsPictureRef.value.files[0])
}

async function fetchSpaceCrafts() {
    loading.value = true;

    try {
        const r = await axios.get("/api/spacecrafts/", {
            params: {
                user_id: filterUser.value === "all" ? null : filterUser.value, // Фильтр по пользователю
                name: filterName.value || null, // Фильтр по названию космического аппарата
                manufacturer: filterManufacturer.value || null, // Фильтр по производителю
                launch_site: filterLaunchSite.value || null, // Фильтр по месту запуска
                mission: filterMission.value || null, // Фильтр по миссии
            },
        });

        spacecrafts.value = r.data;
        console.log(r.data);
    } catch (error) {
        console.error("Ошибка при загрузке космических аппаратов:", error);
    } finally {
        loading.value = false;
    }
}

async function fetchLaunchSites() {
    loading.value = true
    const r = await axios.get("/api/launchsites/");
    launchsites.value = r.data;
    console.log(r.data);
    loading.value = false;
}
async function fetchMissions() {
    loading.value = true
    const r = await axios.get("/api/missions/");
    missions.value = r.data;
    console.log(r.data);
    loading.value = false;
}

async function onSpaceCraftAdd() {

    const formData = new FormData();

    formData.append('picture', spacecraftsPictureRef.value.files[0]);

    formData.set('name', spacecraftToAdd.value.name)
    formData.set('manufacturer', spacecraftToAdd.value.manufacturer)
    formData.set('launch_site', spacecraftToAdd.value.launch_site)
    formData.set('mission', spacecraftToAdd.value.mission)

    await axios.post("/api/spacecrafts/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchSpaceCrafts();

    spacecraftToAdd.value.name = "";
    spacecraftToAdd.value.manufacturer = "";
    spacecraftToAdd.value.launch_site = "";
    spacecraftToAdd.value.mission = "";
    spacecraftAddImageUrl.value = "";

}



// async function onRemoveClick(spacecraft) {
//     this.spacecraftToDelete = spacecraft;
//     const deleteModal = new bootstrap.Modal(document.getElementById('deleteConfirmationModal'));
//     deleteModal.show();
// }
async function confirmDelete() {
    if (this.spacecraftToDelete) {
        await axios.delete(`/api/spacecrafts/${this.spacecraftToDelete.id}/`);
        await this.fetchSpaceCrafts();
        this.spacecraftToDelete = null;
        const deleteModal = bootstrap.Modal.getInstance(document.getElementById('deleteConfirmationModal'));
        deleteModal.hide();
    }
}




async function onRemoveClick(spacecraft) {
    await axios.delete(`/api/spacecrafts/${spacecraft.id}/`);
    spacecraftToDelete.value = null;
    await fetchSpaceCrafts();
}
async function onSpaceCraftEditClick(spacecraft) {
    if (!is2FAEnabled.value) {
        alert("Ошибка 2 факторов");
        return;
    }
    spacecraftToEdit.value = { ...spacecraft };
}
async function onSpaceCraftDeleteClick(spacecraft) {
    spacecraftToDelete.value = { ...spacecraft };
}
// async function onUpdateSpaceCraft() {
//     await axios.put(`/api/spacecrafts/${spacecraftToEdit.value.id}/`, {
//         ...spacecraftToEdit.value
//     });
//     await fetchMissions();
// }


async function onUpdateSpaceCraft() {
    const formData = new FormData();

    // Добавляем данные о космическом аппарате
    formData.set('name', spacecraftToEdit.value.name);
    formData.set('manufacturer', spacecraftToEdit.value.manufacturer);
    formData.set('launch_site', spacecraftToEdit.value.launch_site);
    formData.set('mission', spacecraftToEdit.value.mission);

    // Если было выбрано новое изображение, добавляем его в запрос
    if (newSpacecraftPicture.value) {
        formData.append('picture', newSpacecraftPicture.value);
    }

    // Отправляем запрос
    await axios.put(`/api/spacecrafts/${spacecraftToEdit.value.id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });

    await fetchSpaceCrafts(); // обновляем данные
}

function onEditPictureChange(event) {
    newSpacecraftPicture.value = event.target.files[0]; // сохраняем выбранное изображение
}

// async function onUpdateSpaceCraft() {

// const formData = new FormData();

// formData.append('picture', spacecraftsPictureRef.value.files[0]);

// formData.set('name', spacecraftToEdit.value.name)
// formData.set('manufacturer', spacecraftToEdit.value.manufacturer)
// formData.set('launch_site', spacecraftToEdit.value.launch_site)
// formData.set('mission', spacecraftToEdit.value.mission)

// await axios.put(`/api/spacecrafts/${spacecraftToEdit.value.id}/`, formData, {
//     headers: {
//         'Content-Type': 'multipart/form-data'
//     }
// });
// await fetchSpaceCrafts();
// }



onBeforeMount((async) => {
    fetchUserInfo()
    fetchUsers()
    fetchUsersSpaceCrafts()
    fetchSpaceCrafts() // await
    fetchLaunchSites()
    fetchMissions()
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

// Функция для закрытия модального окна
function closeImageModal() {
    isImageModalVisible.value = false;
}

</script>

<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent.stop="onSpaceCraftAdd" class="p-4 shadow-sm rounded bg-light">
                <div class="row g-3">
                    <!-- Загрузка изображения -->
                    <div class="col-md-12">
                        <div class="d-flex align-items-center">
                            <!-- Поле выбора файла -->
                            <div class="me-3">
                                <input
                                    class="form-control"
                                    type="file"
                                    ref="spacecraftsPictureRef"
                                    @change="spacecraftsAddPictureChange"
                                />
                            </div>
                            <!-- Превью изображения -->
                            <div>
                                <img
                                    :src="spacecraftAddImageUrl"
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
                                id="spacecraft_name"
                                class="form-control"
                                v-model="spacecraftToAdd.name"
                                required
                            />
                            <label for="spacecraft_name">Название</label>
                        </div>
                    </div>
            
                    <!-- Изготовитель -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input
                                type="text"
                                id="spacecraft_manufacturer"
                                class="form-control"
                                v-model="spacecraftToAdd.manufacturer"
                                required
                            />
                            <label for="spacecraft_manufacturer">Изготовитель</label>
                        </div>
                    </div>
            
                    <!-- Космодром -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select
                                id="spacecraft_launch_site"
                                class="form-select"
                                v-model="spacecraftToAdd.launch_site"
                                required
                            >
                                <option :value="p.id" v-for="p in launchsites" :key="p.id">
                                    {{ p.name }}
                                </option>
                            </select>
                            <label for="spacecraft_launch_site">Космодром запуска</label>
                        </div>
                    </div>
            
                    <!-- Миссия -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select
                                id="spacecraft_mission"
                                class="form-select"
                                v-model="spacecraftToAdd.mission"
                                required
                            >
                                <option :value="t.id" v-for="t in missions" :key="t.id">
                                    {{ t.name }}
                                </option>
                            </select>
                            <label for="spacecraft_mission">Миссия</label>
                        </div>
                    </div>
            
                    <!-- Кнопка -->
                    <div class="col-12 text-end">
                        <button class="btn btn-primary">
                            <i class="bi bi-plus-circle"></i> Добавить космический аппарат
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
                            <option :value="u" v-for="u in usersSpaceCrafts" :key="u">{{ usersById[u]?.username }}
                            </option>
                        </select>
                        <label for="user_id">Фильтр по пользователю</label>
                    </div>

                    <div class="row g-3 stats-container">
                        <!-- Количество записей -->
                        <div class="col-md-6">
                            <div class="card shadow-sm h-100">
                                <div class="card-body text-center">
                                    <h5 class="card-title text-primary">
                                        <i class="bi bi-list-ol"></i> Количество записей
                                    </h5>
                                    <p class="card-text fs-4 fw-bold">{{ stat_count }}</p>
                                </div>
                            </div>
                        </div>
                    
                        <!-- Самый популярный производитель -->
                        <div class="col-md-6">
                            <div class="card shadow-sm h-100">
                                <div class="card-body text-center">
                                    <h5 class="card-title text-primary">
                                        <i class="bi bi-star"></i> Самый популярный производитель
                                    </h5>
                                    <p class="card-text fs-5 fw-bold">{{ stat_pop_man }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                </div>
                <div class="p-3 bg-light border rounded shadow-sm">
                    <h5 class="text-primary mb-3">
                        <i class="bi bi-funnel"></i> Фильтры
                    </h5>
                    <div class="row g-3">
                        <!-- Фильтр по названию космического аппарата -->
                        <div class="col-md-3">
                            <div class="form-floating">
                                <input type="text" id="spacecraft_name" class="form-control" v-model="filterName" placeholder="Название космического аппарата" />
                                <label for="spacecraft_name"><i class="bi bi-search"></i> Название</label>
                            </div>
                        </div>
                
                        <!-- Фильтр по производителю -->
                        <div class="col-md-3">
                            <div class="form-floating">
                                <input type="text" id="manufacturer" class="form-control" v-model="filterManufacturer" placeholder="Изготовитель" />
                                <label for="manufacturer"><i class="bi bi-building"></i> Изготовитель</label>
                            </div>
                        </div>
                
                        <!-- Фильтр по космодрому -->
                        <div class="col-md-3">
                            <div class="form-floating">
                                <select id="launch_site" class="form-select" v-model="filterLaunchSite">
                                    <option value="">Все</option>
                                    <option :value="launchSite.id" v-for="launchSite in launchsites" :key="launchSite.id">
                                        {{ launchSite.name }}
                                    </option>
                                </select>
                                <label for="launch_site"><i class="bi bi-geo"></i> Космодром</label>
                            </div>
                        </div>
                
                        <!-- Фильтр по миссии -->
                        <div class="col-md-3">
                            <div class="form-floating">
                                <select id="mission" class="form-select" v-model="filterMission">
                                    <option value="">Все</option>
                                    <option :value="mission.id" v-for="mission in missions" :key="mission.id">
                                        {{ mission.name }}
                                    </option>
                                </select>
                                <label for="mission"><i class="bi bi-rocket"></i> Миссия</label>
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







            <div v-if="loading">Гружу...</div>
            <div>
                <div v-for="item in spacecrafts" class="spacecraft-item border p-3 mb-3">
                    <div class="row">


                        <!-- Название -->
                        <div class="col-6">
                            <strong>Название:</strong>
                            <div>{{ item.name }}</div>
                        </div>

                        <!-- Изображение -->
                        <div class="col-6 mb-3" v-if="item.picture">
                            <strong>Изображение:</strong>
                            <!-- Добавляем обработчик клика на изображение для открытия модального окна -->
                            <div>
                                <img :src="item.picture" alt="Изображение аппарата" style="max-height: 100px;"
                                    class="img-thumbnail" @click="openImageModal(item.picture)">
                            </div>
                        </div>

                        <!-- Изготовитель -->
                        <div class="col-6">
                            <strong>Изготовитель:</strong>
                            <div>{{ item.manufacturer }}</div>
                        </div>

                        <!-- Космодром -->
                        <div class="col-6">
                            <strong>Космодром запуска:</strong>
                            <div>{{ launchsitesById[item.launch_site]?.name }}</div>
                        </div>

                        <!-- Миссия -->
                        <div class="col-12">
                            <strong>Миссия:</strong>
                            <div>{{ missionsById[item.mission]?.name }}</div>
                        </div>

                        <!-- Кнопки редактирования и удаления -->
                        <div class="col-12 mt-2 d-flex justify-content-start gap-2">
                            <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#editSpaceCraftModal"
                                @click="onSpaceCraftEditClick(item)">
                                <i class="bi bi-pencil"></i> Редактировать
                            </button>
                            <button class="btn btn-danger" data-bs-toggle="modal"
                                data-bs-target="#deleteConfirmationModalRef" @click="onSpaceCraftDeleteClick(item)">
                                <i class="bi bi-file-earmark-minus"></i> Удалить
                            </button>
                        </div>
                    </div>
                </div>
            </div>





            <!-- Modal -->
            <div class="modal fade" id="editSpaceCraftModal" tabindex="-1" role="dialog"
                aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Редактирование</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row row-add">
                                <!-- Название -->
                                <div class="col">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="spacecraftToEdit.name"
                                            required>
                                        <label for="floatingInput">Название</label>
                                    </div>
                                </div>

                                <!-- Изготовитель -->
                                <div class="col-auto">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="spacecraftToEdit.manufacturer"
                                            required>
                                        <label for="floatingInput">Изготовитель</label>
                                    </div>
                                </div>

                                <!-- Космодром -->
                                <div class="col-auto">
                                    <div class="form-floating">
                                        <select name="" id="" class="form-select" v-model="spacecraftToEdit.launch_site"
                                            required>
                                            <option :value="p.id" v-for="p in launchsites">{{ p.name }}</option>
                                        </select>
                                        <label for="floatingInput">Космодром запуска</label>
                                    </div>
                                </div>

                                <!-- Миссия -->
                                <div class="col-auto">
                                    <div class="form-floating">
                                        <select name="" id="" class="form-select" v-model="spacecraftToEdit.mission"
                                            required>
                                            <option :value="t.id" v-for="t in missions">{{ t.name }}</option>
                                        </select>
                                        <label for="floatingInput">Миссия</label>
                                    </div>
                                </div>

                                <!-- Текущее изображение -->
                                <div class="col-12 text-center mb-3" v-if="spacecraftToEdit.picture">
                                    <strong>Текущее изображение:</strong>
                                    <div>
                                        <img :src="spacecraftToEdit.picture" alt="Изображение аппарата"
                                            style="max-height: 150px;" class="img-thumbnail">
                                    </div>
                                </div>

                                <!-- Поле для загрузки нового изображения -->
                                <div class="col-12">
                                    <label for="newPicture">Новое изображение</label>
                                    <input type="file" class="form-control" id="newPicture"
                                        @change="onEditPictureChange">
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                                @click="onUpdateSpaceCraft">Сохранить</button>
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
            <div class="modal fade" id="deleteConfirmationModalRef" tabindex="-1" role="dialog"
                aria-labelledby="deleteModalLabel" aria-hidden="true">
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
                            <button type="button" class="btn btn-danger" data-bs-dismiss="modal"
                                @click="onRemoveClick(spacecraftToDelete)">Удалить</button>
                        </div>
                    </div>
                </div>
            </div>




        </div>
    </div>
</template>

<style lang="scss" scoped>
.spacecraft-item {
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