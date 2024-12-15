// import { onBeforeMount, ref } from "vue";
// import axios from "axios";
// import { defineStore } from "pinia";

// const useUserStore = defineStore("UserStore", () => {
//     const is_authenticated = ref(false);
//     const username = ref("");
//     const userId = ref();

//     async function fetchUser() {
//         const r = await axios.get("/api/user/info");
//         is_authenticated.value = r.data.is_authenticated;
//         username.value = r.data.username;
//         userId.value = r.data.userId;
//     }

//     onBeforeMount(() => {
//         fetchUser();
//     });

//     return {
//         is_authenticated,
//         username,
//         userId,
//         fetchUser
//     };
// });

// export default useUserStore;



// import { ref } from "vue";
// import axios from "axios";
// import { defineStore } from "pinia";

// const useUserStore = defineStore("UserStore", () => {
//     const isAuthenticated = ref(false);
//     const username = ref("");
//     const userId = ref(null);

//     async function fetchUser() {
//         try {
//             const response = await axios.get("/api/user-info");
//             isAuthenticated.value = response.data.is_authenticated;
//             username.value = response.data.username || "";
//             userId.value = response.data.user_id || null;
//         } catch (error) {
//             console.error("Error fetching user info:", error);
//             isAuthenticated.value = false;
//             username.value = "";
//             userId.value = null;
//         }
//     }

//     return {
//         isAuthenticated,
//         username,
//         userId,
//         fetchUser,
//     };
// });

// export default useUserStore;




// Хранилище userStore
import { ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";

const useUserStore = defineStore("UserStore", () => {
  const isAuthenticated = ref(false);
  const username = ref("");
  const userId = ref(null);
  const is2Authenticated = ref(false);

  // Функция для получения данных о пользователе
  async function fetchUser() {
    try {
      const response = await axios.get("/api/user/info"); // Запрос для получения информации о пользователе
      // Если пользователь авторизован, обновляем данные
      isAuthenticated.value = response.data.is_authenticated;
      username.value = response.data.username || ""; // Обновляем имя пользователя
      userId.value = response.data.user_id || null;
      is2Authenticated.value = response.otp_authenticated || null;
      console.log("OTP" + response.data.otp_authenticated);
      console.log("Подтянулись данные пользователя");
    } catch (error) {
      console.error("Ошибка при получении данных пользователя:", error);
      isAuthenticated.value = false;
      is2Authenticated.value = false;
      username.value = "";
      userId.value = null;
    }
  }

  // Функция для выхода из системы
  function logout() {
    isAuthenticated.value = false;
    username.value = "";
    userId.value = null;
    localStorage.removeItem('user');
    //Выход из сессии — на сервере обычно это делается через API-запрос
    axios.post("/api/user/logout/").then(() => {
      console.log("Пользователь вышел из системы");
    }).catch((error) => {
      console.error("Ошибка при выходе из системы:", error);
    });
  }

  // Проверка состояния авторизации на основе сессии
  async function checkAuthentication() {
    try {
      await fetchUser();  // Попытка получить информацию о пользователе
      if (isAuthenticated.value) {
        console.log("Пользователь авторизован");
      } else {
        console.log("Неавторизован");
      }
    } catch (error) {
      console.error("Ошибка при проверке авторизации:", error);
      isAuthenticated.value = false;
      username.value = "";
      userId.value = null;
      console.log("Неавторизован");
    }
  }

  return {
    isAuthenticated,
    is2Authenticated,
    username,
    userId,
    fetchUser,
    logout,
    checkAuthentication,  // Экспортируем функцию для явного вызова
  };
});

export default useUserStore;






// import { ref } from "vue";
// import axios from "axios";
// import { defineStore } from "pinia";

// export const useUserStore = defineStore("UserStore", () => {  // Изменено на именованный экспорт
//     const isAuthenticated = ref(false);
//     const username = ref("");
//     const userId = ref(null);

//     async function fetchUser() {
//         try {
//             const response = await axios.get("/api/user/info");
//             isAuthenticated.value = response.data.is_authenticated;
//             username.value = response.data.username || "";
//             userId.value = response.data.user_id || null;
//         } catch (error) {
//             console.error("Error fetching user info:", error);
//             isAuthenticated.value = false;
//             username.value = "";
//             userId.value = null;
//         }
//     }

//     return {
//         isAuthenticated,
//         username,
//         userId,
//         fetchUser,
//     };
// });
