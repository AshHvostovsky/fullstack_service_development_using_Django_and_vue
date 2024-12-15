import { createRouter, createWebHistory } from 'vue-router';
import MissionsView from '../views/MissionsView.vue';
import ProgramsView from '../views/ProgramsView.vue';
import MissionTypesView from '../views/MissionTypesView.vue';
import SpaceCraftsView from '../views/SpaceCraftsView.vue';
import LaunchSitesView from '../views/LaunchSitesView.vue';
import LoginPass from '../views/LoginPass.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "MissionsView",
      component: MissionsView
    },
    {
      path: "/programs",
      name: "ProgramsView",
      component: ProgramsView
    },
    {
      path: "/missiontypes",
      name: "MissionTypesView",
      component: MissionTypesView
    },
    {
      path: "/spacecrafts",
      name: "SpaceCraftsView",
      component: SpaceCraftsView
    },
    {
      path: "/launchsites",
      name: "LaunchSitesView",
      component: LaunchSitesView
    },
    {
      path: "/login",
      name: "LoginPass",
      component: LoginPass
    },

  ]
})

export default router
