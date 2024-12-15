<template>
  <div class="d-flex flex-column min-vh-100">
    <!-- Навигационная панель -->
    <div class="container">
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="/">Миссии<i class="bi bi-rocket-takeoff"></i></a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
          aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">

            <li class="nav-item"><router-link class="nav-link" to="/programs">Программы</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/missiontypes">Типы миссий</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/launchsites">Космодромы</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/spacecrafts">Космические аппараты</router-link></li>
          </div>
          <div class="navbar-nav ms-auto">
            <li v-if="isAuthenticated" class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                aria-expanded="false">
                {{ username }}
              </a>
              <ul class="dropdown-menu">
                <li><strong class="dropdown-item" @click="logout">Выход из аккаунта</strong></li>
              </ul>
            </li>
            <li v-else class="nav-item">
              <router-link class="nav-link" to="/login">Вход</router-link>
            </li>
          </div>
        </div>
      </nav>
    </div>

    <!-- Основной контент -->
    <main class="flex-grow-1 d-flex align-items-stretch">
      <div class="container my-auto">
        <div v-if="!isAuthenticated && route.path !== '/login'" class="alert alert-warning mt-3" role="alert">
          Вы не авторизованы. Пожалуйста, <router-link to="/login" class="alert-link">войдите</router-link>, чтобы
          получить доступ.
        </div>
        <div v-else>
          <router-view />
        </div>
      </div>
    </main>
    <!-- Подвал -->
    <footer class="bg-light text-dark py-4 mt-auto">
      <div class="container">
        <div class="row">
          <div class="col-md-3 mb-3">
            <h5>О проекте</h5>
            <p>Этот веб-проект посвящён космическим программам, миссиям и аппаратам. Исследуйте новые горизонты!</p>
          </div>
          <div class="col-md-3 mb-3">
            <h5>Полезные ссылки</h5>
            <ul class="list-unstyled">
              <li><router-link to="/" class="text-dark">Миссии</router-link></li>
              <li><router-link to="/programs" class="text-dark">Программы</router-link></li>
              <li><router-link to="/missiontypes" class="text-dark">Типы миссий</router-link></li>
              <li><router-link to="/launchsites" class="text-dark">Космодромы</router-link></li>
              <li><router-link to="/spacecrafts" class="text-dark">Космические аппараты</router-link></li>
            </ul>
          </div>
          <div class="col-md-3">
            <h5>Отладка</h5>
            <ul class="list-unstyled ">
              <li><strong>Authenticated:</strong> {{ isAuthenticated }}</li>
              <li><strong>OTPAuthenticated:</strong> {{ is2Authenticated }}</li>
              <li><strong>Username:</strong> {{ username }}</li>
              <li><strong>Route:</strong> {{ route.path }}</li>
              <li><strong @click="logout" style="color: red">Выход из аккаунта</strong></li>
            </ul>
          </div>
          <div class="col-md-3">
            <h5 class="text-primary mb-3">
              <i class="bi bi-download"></i> Скачать данные миссий
            </h5>
            <ul class="list-unstyled">
              <li class="mb-2">
                <button @click="downloadExcel" class="btn btn-outline-success w-100">
                  <i class="bi bi-file-earmark-excel"></i> Скачать Excel
                </button>
              </li>
              <li>
                <button @click="downloadWord" class="btn btn-outline-primary w-100">
                  <i class="bi bi-file-earmark-word"></i> Скачать Word
                </button>
              </li>
            </ul>
          </div>
          
        </div>
 
      </div>
    </footer>
    
  </div>
</template>






<script setup>

import { onMounted } from "vue";
import { storeToRefs } from "pinia";
import useUserStore from "@/stores/userStore";
import { useRoute } from "vue-router";



const userStore = useUserStore();
const { isAuthenticated, username, is2Authenticated } = storeToRefs(userStore);
const route = useRoute();  // Получаем текущий маршрут

const logout = async () => {
  userStore.logout();  // Очистить данные о пользователе в хранилище
  //   router.push('/login');  // Перенаправить на страницу входа
};

// Вызовите checkAuthentication при монтировании компонента
onMounted(() => {
  userStore.checkAuthentication();
});
async function downloadExcel() {
    window.open('/api/missions/export-excel/', '_blank');
}

async function downloadWord() {
    window.open('/api/missions/export-word/', '_blank');
}


</script>

<style lang="scss" scoped>
html,
body {
  height: 100%;
  margin: 0;
}

.d-flex {
  display: flex;
}

.flex-column {
  flex-direction: column;
}

.min-vh-100 {
  min-height: 100vh;
}

.flex-grow-1 {
  flex: 1;
}

main {
  display: flex;
  flex-direction: column;
}

.my-auto {
  margin-top: auto;
  margin-bottom: auto;
}

</style>




<!--   
  <template>
    <div class="container">
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="#">Главная<i class="bi bi-rocket-takeoff"></i></a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup"
                aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/">Миссии</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/programs">Программы</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/missiontypes">Типы миссий</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/launchsites">Космодромы</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/spacecrafts">Космические аппараты</router-link>
                    </li>
                </div>
        
                
                
                <div class="navbar-nav ms-auto">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Пользователь
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/admin">Админка</a></li>
                        </ul>
                    </li>
                </div>


            </div>
        </nav>
        
    </div>
    <div class="container">
        <router-view/>
    </div>
</template> -->