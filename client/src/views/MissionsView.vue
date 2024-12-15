<script setup>
import { computed, ref, onBeforeMount, watch } from 'vue';
import axios from "axios"
import _ from 'lodash';
import { debounce } from 'lodash';





import Cookies from 'js-cookie';

const csrfToken = Cookies.get('csrftoken');

axios.defaults.headers.common['X-CSRFToken'] = csrfToken;





const missions = ref([]);
const programs = ref([]);
const mission_types = ref([]);
const missionToAdd = ref([]);
const missionToEdit = ref([]);
const missionToDelete = ref([]);

const isSuperUser = ref(false);
const usersMissions = ref([]);
const users = ref([]);

const loading = ref(false);

const stat_count = ref();
const stat_avg = ref();
const stat_max = ref();
const stat_min = ref();
const stat_pop_pr = ref();

const filterUser = ref(null);
const filterName = ref("");
const filterDate = ref(null);
const filterOutcome = ref("");
const filterDecription = ref("");
const filterProgram = ref(null);
const filterType = ref(null);

function resetFilters() {
        filterName.value = "";
        filterDate.value = null;
        filterOutcome.value = "";
        filterDecription.value = "";
        filterProgram.value = null;
        filterType.value = null;

        // Перезапускаем запрос миссий
        fetchMissions();
};

watch(
    [filterName, filterDate, filterOutcome, filterDecription, filterProgram, filterType, filterUser],
    (newValues, oldValues) => {
        console.log("Фильтры изменились:", newValues); // Лог для проверки
        fetchMissions();
    },
    { immediate: true } // Запуск при монтировании
);


async function fetchStats() {
    // Выполняем запрос для получения всех пользователей
    const response = await axios.get("/api/missions/stats"); // Запрос к вашему API
    stat_count.value = response.data.count
    stat_avg.value = response.data.avg
    stat_max.value = response.data.max
    stat_min.value = response.data.min
    stat_pop_pr.value = response.data.popular_program.space_program__name
    console.log(stat_count)
}

const programsById = computed(() => {
    return _.keyBy(programs.value, x => x.id)
})
const typesById = computed(() => {
    return _.keyBy(mission_types.value, x => x.id)
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
async function fetchUsersMissions() {
    // Выполняем запрос для получения всех программ
    const r = await axios.get("/api/missions/", {
        params: {
            user_id: null, // Получаем все программы без фильтра по пользователю
        }
    });

    // Обновляем список программ (если это нужно)
    missions.value = r.data;

    // Используем Set для уникальных пользователей
    const usersSet = new Set();

    // Итерируем по каждой программе и добавляем уникальных пользователей в Set
    r.data.forEach(mission => {
        if (mission.user) {
            usersSet.add(mission.user); // Добавляем пользователя, если он существует
        }
    });

    // Преобразуем Set в массив и записываем в ref переменную
    usersMissions.value = Array.from(usersSet);

    // Для проверки выводим список пользователей в консоль
    console.log(usersMissions.value);
}
async function fetchUsers() {
    // Выполняем запрос для получения всех пользователей
    const response = await axios.get("/api/users/"); // Запрос к вашему API
    users.value = response.data; // Сохраняем пользователей в переменной
    console.log(users.value)
}

async function fetchPrograms() {
    loading.value = true
    const r = await axios.get("/api/spaceprograms/");
    programs.value = r.data;
    console.log(r.data);
    loading.value = false;
}
async function fetchTypes() {
    loading.value = true
    const r = await axios.get("/api/missiontypes/");
    mission_types.value = r.data;
    console.log(r.data);
    loading.value = false;
}
async function fetchMissions() {
    loading.value = true;

    try {
        const r = await axios.get("/api/missions/", {
            params: {
                user_id: filterUser.value === "all" ? null : filterUser.value, // Фильтр по пользователю
                name: filterName.value || null, // Фильтр по названию миссии
                date: filterDate.value || null, // Фильтр по дате запуска
                outcome: filterOutcome.value || null, // Фильтр по исходу
                description: filterDecription.value || null, // Фильтр по описанию
                program: filterProgram.value || null, // Фильтр по программе
                type: filterType.value || null, // Фильтр по типу миссии
            },
        });

        missions.value = r.data;
        console.log(r.data);
    } catch (error) {
        console.error("Ошибка при загрузке миссий:", error);
    } finally {
        loading.value = false;
    }
}


async function onMissionAdd() {
    // await axios.post("/api/missions/", {
    //     name : "test",
    //     launch_date: "Дата старта",
    //     end_date: "Дата окончания",
    //     outcome: "Исход",
    //     description: "Описание",
    //     space_program: "1",
    //     mission_type: "1"
    // });

    await axios.post("/api/missions/", {
        ...missionToAdd.value,
    });
    await fetchMissions();

    missionToAdd.value.name = "";
    missionToAdd.value.launch_date = "";
    missionToAdd.value.outcome = "";
    missionToAdd.value.description = "";
    missionToAdd.value.space_program = "";
    missionToAdd.value.mission_type = "";
}
async function onRemoveClick(mission) {
    await axios.delete(`/api/missions/${mission.id}/`);
    missionToDelete.value = null;
    await fetchMissions();
}
async function onMissionDeleteClick(mission) {
    missionToDelete.value = { ...mission };
}
async function onMissionEditClick(mission) {
    missionToEdit.value = { ...mission };
}
async function onUpdateMission() {
    await axios.put(`/api/missions/${missionToEdit.value.id}/`, {
        ...missionToEdit.value
    });
    await fetchMissions();
}


onBeforeMount((async) => {
    fetchUserInfo()
    fetchUsers()
    fetchUsersMissions()
    fetchMissions() // await
    fetchPrograms()
    fetchTypes()
    fetchStats()
})

</script>


<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent.stop="onMissionAdd" class="p-4 shadow-sm rounded bg-light">
                <div class="row g-3">
                    <!-- Название миссии -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" id="mission_name" class="form-control" v-model="missionToAdd.name"
                                required>
                            <label for="mission_name">Название</label>
                        </div>
                    </div>

                    <!-- Дата старта -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="date" id="launch_date" class="form-control" v-model="missionToAdd.launch_date"
                                required>
                            <label for="launch_date">Дата старта</label>
                        </div>
                    </div>

                    <!-- Исход миссии -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" id="mission_outcome" class="form-control" v-model="missionToAdd.outcome"
                                required>
                            <label for="mission_outcome">Исход</label>
                        </div>
                    </div>

                    <!-- Программа -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select id="space_program" class="form-select" v-model="missionToAdd.space_program"
                                required>
                                <option :value="p.id" v-for="p in programs" :key="p.id">{{ p.name }}</option>
                            </select>
                            <label for="space_program">Программа</label>
                        </div>
                    </div>

                    <!-- Тип миссии -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select id="mission_type" class="form-select" v-model="missionToAdd.mission_type" required>
                                <option :value="t.id" v-for="t in mission_types" :key="t.id">{{ t.name }}</option>
                            </select>
                            <label for="mission_type">Тип миссии</label>
                        </div>
                    </div>

                    <!-- Описание -->
                    <div class="col-12">
                        <div class="form-floating">
                            <textarea id="mission_description" class="form-control" v-model="missionToAdd.description"
                                style="height: 100px;" required></textarea>
                            <label for="mission_description">Описание</label>
                        </div>
                    </div>

                    <!-- Кнопка -->
                    <div class="col-12 text-end">
                        <button class="btn btn-primary">
                            <i class="bi bi-plus-circle"></i> Добавить миссию
                        </button>
                    </div>
                </div>
            </form>



            <div class="col-auto mt-4">
                <div v-if="isSuperUser.value == true">
                    <!-- Фильтр по пользователю-->
                    <div class="form-floating filter mb-3">
                        <select name="user_id" id="user_id" class="form-select" v-model="filterUser">
                            <option value="all">Все</option>
                            <!-- Выводим список уникальных пользователей -->
                            <option :value="u" v-for="u in usersMissions" :key="u">{{ usersById[u]?.username }}</option>
                        </select>
                        <label for="user_id">Фильтр по пользователю</label>
                    </div>


                    <!-- Статистика -->
                    <div class="stats-container row g-3">
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
                        <div class="col-md-6">
                            <div class="card shadow-sm h-100">
                                <div class="card-body text-center">
                                    <h5 class="card-title text-primary">
                                        <i class="bi bi-star"></i> Самая популярная программа
                                    </h5>
                                    <p class="card-text fs-5 fw-bold">{{ stat_pop_pr }}</p>
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
                        <!-- Фильтр по названию миссии -->
                        <div class="col-md-2">
                            <div class="form-floating">
                                <input type="text" id="mission_name" class="form-control" v-model="filterName"
                                    placeholder="Название миссии" />
                                <label for="mission_name"><i class="bi bi-search"></i> Название миссии</label>
                            </div>
                        </div>

                        <!-- Фильтр по дате запуска -->
                        <div class="col-md-2">
                            <div class="form-floating">
                                <input type="date" id="launch_date" class="form-control" v-model="filterDate" />
                                <label for="launch_date"><i class="bi bi-calendar"></i> Дата запуска</label>
                            </div>
                        </div>

                        <!-- Фильтр по исходу -->
                        <div class="col-md-2">
                            <div class="form-floating">
                                <input type="text" id="outcome" class="form-control" v-model="filterOutcome"
                                    placeholder="Исход" />
                                <label for="outcome"><i class="bi bi-flag"></i> Исход</label>
                            </div>
                        </div>

                        <!-- Фильтр по описанию -->
                        <div class="col-md-2">
                            <div class="form-floating">
                                <input type="text" id="description" class="form-control" v-model="filterDecription"
                                    placeholder="Описание" />
                                <label for="description"><i class="bi bi-chat-text"></i> Описание</label>
                            </div>
                        </div>

                        <!-- Фильтр по программе -->
                        <div class="col-md-2">
                            <div class="form-floating">
                                <select id="program" class="form-select" v-model="filterProgram">
                                    <option value="">Все</option>
                                    <option :value="program.id" v-for="program in programs" :key="program.id">
                                        {{ program.name }}
                                    </option>
                                </select>
                                <label for="program"><i class="bi bi-bookmark"></i> Программа</label>
                            </div>
                        </div>

                        <!-- Фильтр по типу миссии -->
                        <div class="col-md-2">
                            <div class="form-floating">
                                <select id="mission_type" class="form-select" v-model="filterType">
                                    <option value="">Все</option>
                                    <option :value="type.id" v-for="type in mission_types" :key="type.id">
                                        {{ type.name }}
                                    </option>
                                </select>
                                <label for="mission_type"><i class="bi bi-geo"></i> Тип миссии</label>
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
                <div v-for="item in missions" class="mission-item border p-3 mb-3">
                    <div class="row">
                        <!-- Название миссии -->
                        <div class="col-12">
                            <strong>Название миссии:</strong>
                            <div>{{ item.name }}</div>
                        </div>

                        <!-- Дата запуска -->
                        <div class="col-6">
                            <strong>Дата запуска:</strong>
                            <div>{{ item.launch_date }}</div>
                        </div>

                        <!-- Исход миссии -->
                        <div class="col-6">
                            <strong>Исход:</strong>
                            <div>{{ item.outcome }}</div>
                        </div>

                        <!-- Описание миссии -->
                        <div class="col-12">
                            <strong>Описание:</strong>
                            <div>{{ item.description }}</div>
                        </div>

                        <!-- Программа миссии -->
                        <div class="col-6">
                            <strong>Программа:</strong>
                            <div>{{ programsById[item.space_program]?.name }}</div>
                        </div>

                        <!-- Тип миссии -->
                        <div class="col-6">
                            <strong>Тип миссии:</strong>
                            <div>{{ typesById[item.mission_type]?.name }}</div>
                        </div>

                        <!-- Кнопки редактирования и удаления -->
                        <div class="col-12 mt-2 d-flex justify-content-end gap-2">
                            <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#editMissionModal"
                                @click="onMissionEditClick(item)">
                                <i class="bi bi-pencil"></i> Редактировать
                            </button>
                            <button class="btn btn-danger" data-bs-toggle="modal"
                                data-bs-target="#deleteConfirmationModalRef" @click="onMissionDeleteClick(item)">
                                <i class="bi bi-file-earmark-minus"></i> Удалить
                            </button>
                        </div>
                    </div>
                </div>
            </div>





            <!-- Modal -->
            <div class="modal fade" id="editMissionModal" tabindex="-1" role="dialog"
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
                                        <input type="text" class="form-control" v-model="missionToEdit.name" required>
                                        <label for="floatingInput">Название</label>
                                    </div>
                                </div>


                                <div class="col-auto">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="missionToEdit.launch_date"
                                            required>
                                        <label for="floatingInput">Дата старта</label>
                                    </div>
                                </div>
                                <div class="col-auto">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="missionToEdit.outcome"
                                            required>
                                        <label for="floatingInput">Исход</label>
                                    </div>
                                </div>
                                <div class="col-auto">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="missionToEdit.description"
                                            required>
                                        <label for="floatingInput">Описание</label>
                                    </div>
                                </div>


                                <div class="col-auto">
                                    <div class="form-floating">
                                        <select name="" id="" class="form-select" v-model="missionToEdit.space_program"
                                            required>
                                            <option :value="p.id" v-for="p in programs">{{ p.name }}</option>
                                        </select>
                                        <label for="floatingInput">Программа</label>
                                    </div>
                                </div>

                                <div class="col-auto">
                                    <div class="form-floating">
                                        <select name="" id="" class="form-select" v-model="missionToEdit.mission_type"
                                            required>
                                            <option :value="t.id" v-for="t in mission_types">{{ t.name }}</option>
                                        </select>
                                        <label for="floatingInput">Тип миссии</label>
                                    </div>
                                </div>


                            </div>

                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                                @click="onUpdateMission">Сохранить</button>
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
                                @click="onRemoveClick(missionToDelete)">Удалить</button>
                        </div>
                    </div>
                </div>
            </div>



        </div>
    </div>
</template>





<style lang="scss" scoped>
.mission-item {
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