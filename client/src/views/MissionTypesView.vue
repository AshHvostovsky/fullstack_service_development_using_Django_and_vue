<script setup>
import { computed, ref, onBeforeMount, watch } from 'vue';
import axios from "axios"
import _ from 'lodash';

const missiontypes = ref([])
const missiontypeToAdd = ref([])
const missiontypeToEdit = ref([])
const missiontypeToDelete = ref([]);

const isSuperUser = ref(false);
const usersTypes = ref([]);
const users = ref([]);

const loading = ref(false);

const stat_count = ref();
const stat_avg = ref();
const stat_max = ref();
const stat_min = ref();

const filterUser = ref(null);
const filterName = ref("");

function resetFilters() {
        filterName.value = "";
        // Перезапускаем запрос миссий
        fetchMissionTypes();
};

watch(
    [filterName, filterUser],
    (newValues, oldValues) => {
        console.log("Фильтры изменились:", newValues); // Лог для проверки
        fetchMissionTypes();
    },
    { immediate: true } // Запуск при монтировании
);

async function fetchStats() {
    // Выполняем запрос для получения всех пользователей
    const response = await axios.get("/api/missiontypes/stats"); // Запрос к вашему API
    stat_count.value = response.data.count
    stat_avg.value = response.data.avg
    stat_max.value = response.data.max
    stat_min.value = response.data.min
    console.log(stat_count)
}

const missiontypesById = computed(() => {
    return _.keyBy(missiontypes.value, x => x.id)
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
async function fetchUsersTypes() {
    // Выполняем запрос для получения всех программ
    const r = await axios.get("/api/missiontypes/", {
        params: {
            user_id: null, // Получаем все программы без фильтра по пользователю
        }
    });

    // Обновляем список программ (если это нужно)
    missiontypes.value = r.data;

    // Используем Set для уникальных пользователей
    const usersSet = new Set();

    // Итерируем по каждой программе и добавляем уникальных пользователей в Set
    r.data.forEach(missiontype => {
        if (missiontype.user) {
            usersSet.add(missiontype.user); // Добавляем пользователя, если он существует
        }
    });

    // Преобразуем Set в массив и записываем в ref переменную
    usersTypes.value = Array.from(usersSet);

    // Для проверки выводим список пользователей в консоль
    console.log(usersTypes.value);
}
async function fetchUsers() {
    // Выполняем запрос для получения всех пользователей
    const response = await axios.get("/api/users/"); // Запрос к вашему API
    users.value = response.data; // Сохраняем пользователей в переменной
    console.log(users.value)
}

async function fetchMissionTypes() {
    loading.value = true;

    try {
        const r = await axios.get("/api/missiontypes/", {
            params: {
                user_id: filterUser.value === "all" ? null : filterUser.value, // Фильтр по пользователю
                name: filterName.value || null, // Фильтр по названию типа миссии
            },
        });

        missiontypes.value = r.data;
        console.log(r.data);
    } catch (error) {
        console.error("Ошибка при загрузке типов миссий:", error);
    } finally {
        loading.value = false;
    }
}


async function onMissionTypeAdd() {
    await axios.post("/api/missiontypes/", {
        ...missiontypeToAdd.value,
    });
    await fetchMissionTypes();

    missiontypeToAdd.value.name = "";

}
async function onRemoveClick(missiontype) {
    await axios.delete(`/api/missiontypes/${missiontype.id}/`);
    missiontypeToDelete.value = null;
    await fetchMissionTypes();
}
async function onMissionTypeDeleteClick(missiontype) {
    missiontypeToDelete.value = { ...missiontype };
}
async function onMissionTypeEditClick(missiontype) {
    missiontypeToEdit.value = { ...missiontype };
}
async function onUpdateMissionType() {
    await axios.put(`/api/missiontypes/${missiontypeToEdit.value.id}/`, {
        ...missiontypeToEdit.value
    });
    await fetchMissionTypes();
}
onBeforeMount((async) => {
    fetchUserInfo()
    fetchUsers()
    fetchUsersTypes()
    fetchMissionTypes(); //await
    fetchStats()
})
</script>

<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent.stop="onMissionTypeAdd" class="p-4 shadow-sm rounded bg-light">
                <div class="row g-3">
                    <!-- Название типа миссии -->
                    <div class="col-md-12">
                        <div class="form-floating">
                            <input type="text" id="mission_type_name" class="form-control"
                                v-model="missiontypeToAdd.name" required />
                            <label for="mission_type_name">Название</label>
                        </div>
                    </div>

                    <!-- Кнопка -->
                    <div class="col-12 text-end">
                        <button class="btn btn-primary">
                            <i class="bi bi-plus-circle"></i> Добавить тип миссии
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
                            <option :value="u" v-for="u in usersTypes" :key="u">{{ usersById[u]?.username }}</option>
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

                </div>
                <div class="p-3 bg-light border rounded shadow-sm">
                    <h5 class="text-primary mb-3">
                        <i class="bi bi-funnel"></i> Фильтр
                    </h5>
                    <div class="row g-3">
                        <!-- Фильтр по названию типа миссии -->
                        <div class="col-md-12">
                            <div class="form-floating">
                                <input type="text" id="mission_type_name" class="form-control" v-model="filterName"
                                    placeholder="Название типа миссии" />
                                <label for="mission_type_name"><i class="bi bi-search"></i> Название типа миссии</label>
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
                <div v-for="item in missiontypes" class="missiontype-item border p-3 mb-3">
                    <div class="row">
                        <!-- Название миссии -->
                        <div class="col-12">
                            <strong>Название:</strong>
                            <div>{{ item.name }}</div>
                        </div>



                        <!-- Кнопки редактирования и удаления -->
                        <div class="col-12 mt-2 d-flex justify-content-start gap-2">
                            <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#editMissionTypeModal"
                                @click="onMissionTypeEditClick(item)">
                                <i class="bi bi-pencil"></i> Редактировать
                            </button>
                            <button class="btn btn-danger" data-bs-toggle="modal"
                                data-bs-target="#deleteConfirmationModalRef" @click="onMissionTypeDeleteClick(item)">
                                <i class="bi bi-file-earmark-minus"></i> Удалить
                            </button>
                        </div>
                    </div>
                </div>
            </div>





            <!-- Modal -->
            <div class="modal fade" id="editMissionTypeModal" tabindex="-1" role="dialog"
                aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Редактирование</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                                <!-- <span aria-hidden="true">&times;</span> -->
                            </button>
                        </div>
                        <div class="modal-body">

                            <div class="row row-add">
                                <div class="col">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="missiontypeToEdit.name"
                                            required>
                                        <label for="floatingInput">Название</label>
                                    </div>


                                </div>

                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                                    @click="onUpdateMissionType">Сохранить</button>
                            </div>
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
                                @click="onRemoveClick(missiontypeToDelete)">Удалить</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.missiontype-item {
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