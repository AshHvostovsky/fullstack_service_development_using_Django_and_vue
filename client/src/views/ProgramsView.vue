<script setup>
import { computed, ref, onBeforeMount, watch } from 'vue';
import axios from "axios"
import _ from 'lodash';

const programs = ref([])
const programToAdd = ref([])
const programToEdit = ref([])
const programToDelete = ref([]);

const isSuperUser = ref(false);
const usersPrograms = ref([]);
const users = ref([]);


const loading = ref(false);

const stat_count = ref();
const stat_avg = ref();
const stat_max = ref();
const stat_min = ref();
const stat_long_pr = ref();

const filterUser = ref(null);
const filterName = ref("");
const filterDateStart = ref("");
const filterDateEnd = ref("");
const filterDecription = ref("");

function resetFilters() {
        filterName.value = "";
        filterDateStart.value = null;
        filterDateEnd.value = null;
        filterDecription.value = "";
        // Перезапускаем запрос миссий
        fetchPrograms();
};
watch(
    [filterName, filterDateStart, filterDateEnd, filterDecription, filterUser],
    (newValues, oldValues) => {
        console.log("Фильтры изменились:", newValues); // Лог для проверки
        fetchPrograms();
    },
    { immediate: true } // Запуск при монтировании
);


async function fetchStats() {
    // Выполняем запрос для получения всех пользователей
    const response = await axios.get("/api/spaceprograms/stats"); // Запрос к вашему API
    stat_count.value = response.data.count
    stat_avg.value = response.data.avg
    stat_max.value = response.data.max
    stat_min.value = response.data.min
    stat_long_pr.value = response.data.longest_mission_name
    console.log(stat_count)
}

const programsById = computed(() => {
    return _.keyBy(programs.value, x => x.id)
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
async function fetchUsersPrograms() {
    // Выполняем запрос для получения всех программ
    const r = await axios.get("/api/spaceprograms/", {
        params: {
            user_id: null, // Получаем все программы без фильтра по пользователю
        }
    });

    // Обновляем список программ (если это нужно)
    programs.value = r.data;

    // Используем Set для уникальных пользователей
    const usersSet = new Set();

    // Итерируем по каждой программе и добавляем уникальных пользователей в Set
    r.data.forEach(program => {
        if (program.user) {
            usersSet.add(program.user); // Добавляем пользователя, если он существует
        }
    });

    // Преобразуем Set в массив и записываем в ref переменную
    usersPrograms.value = Array.from(usersSet);

    // Для проверки выводим список пользователей в консоль
    console.log(usersPrograms.value);
}
async function fetchUsers() {
    // Выполняем запрос для получения всех пользователей
    const response = await axios.get("/api/users/"); // Запрос к вашему API
    users.value = response.data; // Сохраняем пользователей в переменной
    console.log(users.value)
}

async function fetchPrograms() {
    loading.value = true;

    try {
        const response = await axios.get("/api/spaceprograms/", {
            params: {
                user_id: filterUser.value === "all" ? null : filterUser.value, // Фильтр по пользователю
                name: filterName.value || null, // Фильтр по названию программы
                start_date: filterDateStart.value || null, // Фильтр по дате запуска
                end_date: filterDateEnd.value || null, // Фильтр по дате окончания
                description: filterDecription.value || null, // Фильтр по описанию
            },
        });

        programs.value = response.data; // Привязка данных программ
        console.log(response.data);
    } catch (error) {
        console.error("Ошибка при загрузке программ:", error);
    } finally {
        loading.value = false;
    }
}



async function onProgramAdd() {
    await axios.post("/api/spaceprograms/", {
        ...programToAdd.value,
    });
    await fetchPrograms();

    programToAdd.value.name = "";
    programToAdd.value.start_date = "";
    programToAdd.value.end_date = "";
    programToAdd.value.description = "";
}
async function onRemoveClick(program) {
    await axios.delete(`/api/spaceprograms/${program.id}/`);
    programToDelete.value = null;
    await fetchPrograms();
}
async function onProgramDeleteClick(program) {
    programToDelete.value = { ...program };
}
async function onProgramEditClick(program) {
    programToEdit.value = { ...program };
}
async function onUpdateProgram() {
    await axios.put(`/api/spaceprograms/${programToEdit.value.id}/`, {
        ...programToEdit.value
    });
    await fetchPrograms();
}
onBeforeMount((async) => {
    fetchUserInfo()
    fetchUsers()
    fetchUsersPrograms()
    fetchPrograms(); //await
    fetchStats()

})
</script>

<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent.stop="onProgramAdd" class="p-4 shadow-sm rounded bg-light">
                <div class="row g-3">
                    <!-- Название программы -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" id="program_name" class="form-control" v-model="programToAdd.name"
                                required />
                            <label for="program_name">Название</label>
                        </div>
                    </div>

                    <!-- Дата старта -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="date" id="start_date" class="form-control" v-model="programToAdd.start_date"
                                required />
                            <label for="start_date">Дата старта</label>
                        </div>
                    </div>

                    <!-- Дата окончания -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="date" id="end_date" class="form-control" v-model="programToAdd.end_date"
                                required />
                            <label for="end_date">Дата окончания</label>
                        </div>
                    </div>

                    <!-- Описание программы -->
                    <div class="col-12">
                        <div class="form-floating">
                            <textarea id="program_description" class="form-control" v-model="programToAdd.description"
                                style="height: 100px;" required></textarea>
                            <label for="program_description">Описание</label>
                        </div>
                    </div>

                    <!-- Кнопка -->
                    <div class="col-12 text-end">
                        <button class="btn btn-primary">
                            <i class="bi bi-plus-circle"></i> Добавить программу
                        </button>
                    </div>
                </div>
            </form>





            <div class="col-auto mt-4">
                <div v-if="isSuperUser.value == true">
                    <!-- Фильтр -->
                    <div class="form-floating filter mb-3">
                        <select name="user_id" id="user_id" class="form-select" v-model="filterUser">
                            <option value="all">Все</option>
                            <!-- Выводим список уникальных пользователей -->
                            <option :value="u" v-for="u in usersPrograms" :key="u">{{ usersById[u]?.username }}</option>
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
                        <i class="bi bi-funnel"></i> Фильтры
                    </h5>
                    <div class="row g-3">
                        <!-- Фильтр по названию программы -->
                        <div class="col-md-3">
                            <div class="form-floating">
                                <input type="text" id="program_name" class="form-control" v-model="filterName"
                                    placeholder="Название программы" />
                                <label for="program_name"><i class="bi bi-search"></i> Название программы</label>
                            </div>
                        </div>
                
                        <!-- Фильтр по дате запуска -->
                        <div class="col-md-3">
                            <div class="form-floating">
                                <input type="date" id="start_date" class="form-control" v-model="filterDateStart" />
                                <label for="start_date"><i class="bi bi-calendar"></i> Дата запуска</label>
                            </div>
                        </div>
                
                        <!-- Фильтр по дате окончания -->
                        <div class="col-md-3">
                            <div class="form-floating">
                                <input type="date" id="end_date" class="form-control" v-model="filterDateEnd" />
                                <label for="end_date"><i class="bi bi-calendar-x"></i> Дата окончания</label>
                            </div>
                        </div>
                
                        <!-- Фильтр по описанию -->
                        <div class="col-md-3">
                            <div class="form-floating">
                                <input type="text" id="description" class="form-control" v-model="filterDecription"
                                    placeholder="Описание" />
                                <label for="description"><i class="bi bi-chat-text"></i> Описание</label>
                            </div>
                        </div>
                    </div>
                
                    <!-- Кнопка сброса фильтров -->
                    <div class="row mt-3">
                        <div class="col text-end">
                            <button class="btn btn-outline-secondary" @click="resetFilters">
                                <i class="bi bi-arrow-counterclockwise"></i> Сбросить фильтры
                            </button>
                        </div>
                    </div>
                </div>
                
            </div>



            <div v-if="loading">Гружу...</div>
            <div>
                <div v-for="item in programs" class="program-item border p-3 mb-3">
                    <div class="row">
                        <!-- Название миссии -->
                        <div class="col-12">
                            <strong>Название программы:</strong>
                            <div>{{ item.name }}</div>
                        </div>

                        <!-- Дата запуска -->
                        <div class="col-6">
                            <strong>Дата запуска:</strong>
                            <div>{{ item.start_date }}</div>
                        </div>

                        <!-- Дата окончания -->
                        <div class="col-6">
                            <strong>Дата окончания:</strong>
                            <div>{{ item.end_date }}</div>
                        </div>

                        <!-- Описание -->
                        <div class="col-12">
                            <strong>Описание:</strong>
                            <div>{{ item.description }}</div>
                        </div>

                        <!-- Кнопки редактирования и удаления -->
                        <div class="col-12 mt-2 d-flex justify-content-start gap-2">
                            <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#editProgramModal"
                                @click="onProgramEditClick(item)">
                                <i class="bi bi-pencil"></i> Редактировать
                            </button>
                            <button class="btn btn-danger" data-bs-toggle="modal"
                                data-bs-target="#deleteConfirmationModalRef" @click="onProgramDeleteClick(item)">
                                <i class="bi bi-file-earmark-minus"></i> Удалить
                            </button>
                        </div>
                    </div>
                </div>
            </div>





            <!-- Modal -->
            <div class="modal fade" id="editProgramModal" tabindex="-1" role="dialog"
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
                                        <input type="text" class="form-control" v-model="programToEdit.name" required>
                                        <label for="floatingInput">Название</label>
                                    </div>
                                </div>


                                <div class="col-auto">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="programToEdit.start_date"
                                            required>
                                        <label for="floatingInput">Дата старта</label>
                                    </div>
                                </div>
                                <div class="col-auto">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="programToEdit.end_date"
                                            required>
                                        <label for="floatingInput">Дата окончания</label>
                                    </div>
                                </div>
                                <div class="col-auto">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="programToEdit.description"
                                            required>
                                        <label for="floatingInput">Описание</label>
                                    </div>
                                </div>



                            </div>

                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                                @click="onUpdateProgram">Сохранить</button>
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
                                @click="onRemoveClick(programToDelete)">Удалить</button>
                        </div>
                    </div>
                </div>
            </div>


        </div>
    </div>

</template>

<style lang="scss" scoped>
.program-item {
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