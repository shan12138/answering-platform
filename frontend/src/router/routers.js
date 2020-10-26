import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import AdminHome from '../components/views/AdminHome'
import TeacherInforMng from '../components/admin/TeacherInforMng'
import DepartmentsInforMng from '../components/admin/DepartmentsInforMng'
import AdminLogin from '../components/admin/AdminLogin'
import TeacherLog from '../components/admin/TeacherLog'
import StudentLog from '../components/admin/StudentLog'
import StudentFrame from '../components/StudentFrame'
import StudentHome from '../components/student/Home'
import TeacherHome from '../components/teacher/Home'
import StudentLivingRoom from '../components/views/StudentLivingRoom'
import TeacherLivingRoom from '../components/views/TeacherLivingRoom'
import ModifyStuInfo from '../components/modify_user_info/ModifyStuInfo'
import ModifyTeaInfo from '../components/modify_user_info/ModifyTeaInfo'
import CreateRoom from '../components/room/CreateRoom.vue'
import TeacherLogin from '../components/teacher/TeacherLogin'
import StudentLogin from '../components/student/StudentLogin'
import TeacherFrame from '../components/TeacherFrame'
import Register from '../components/Register'
import ModifyRoomInfo from '../components/tea_mng_room/ModifyRoomInfo'
import ListParticipateRoom from '../components/tea_mng_room/ListParticipateRoom'
import ManageTimetable from '../components/timetable/ManageTimetable'
import StudentLivingRoomInfo from '../components/views/StudentLivingRoomInfo'
import TeacherLivingRoomInfo from '../components/views/TeacherLivingRoomInfo'
const routes = [
  {
    path: '/register',
    name: 'register',
    component: Register
  },

  {
    path: '/student',
    name: 'studentLogin',
    component: StudentLogin
  },

  {
    path: '/student/Frame',
    name: 'student',
    component: StudentFrame,
    redirect: '/student/Home',
    children: [
      {
        path: '/student/Home',
        name: 'studentHome',
        component: StudentHome,
      },
      {
        path: '/student/Info',
        name: 'ModifyStuInfo',
        component: ModifyStuInfo
      },
      {
        path: '/student/LivingRoomInfo',
        name: 'LivingRoomInfo',
        component: StudentLivingRoomInfo
      },
      {
        path: '/student/livingRoom',
        component: StudentLivingRoom
      },
    ],
  },
  {
    path: '/admin',
    name: 'adminLogin',
    component: AdminLogin,
  },
  {
    path: '/admin/home',
    name: 'admin',
    component: AdminHome,
    redirect: '/admin/home/teacherInforMng',
    children: [
      {
        path: 'teacherInforMng',
        name: 'teacherInfor',
        component: TeacherInforMng,
      },
      {
        path: 'departmentsInforMng',
        component: DepartmentsInforMng,
      },
      {
        path: 'teacherLog',
        component: TeacherLog,
      },
      {
        path: 'studentLog',
        component: StudentLog,
      },
    ],
  },
  {
    path: '/teacher',
    name: 'teacherLogin',
    component: TeacherLogin,
  },
  {
    path: '/teacher/Frame',
    name: 'teacher',
    component: TeacherFrame,
    redirect: '/teacher/Home',
    children: [
      {
        path: '/teacher/Home',
        name: 'teacherHome',
        component: TeacherHome,
      },
      {
        path: '/teacher/Info',
        name: 'ModifyTeaInfo',
        component: ModifyTeaInfo,
      },
      {
        path: '/teacher/ListParticipateRoom',
        name: 'listParticipateRoom',
        component: ListParticipateRoom
      },
      {
        path: '/teacher/LivingRoomInfo',
        name: 'LivingRoomInfo',
        component: TeacherLivingRoomInfo
      },
      {
        path: '/teacher/CreateRoom',
        component: CreateRoom
      },
      {
        path: '/teacher/ManageTimetable',
        component: ManageTimetable
      },
      {
        path: '/teacher/ModifyRoomInfo',
        name: 'modifyRoomInfo',
        component: ModifyRoomInfo
      },
      {
        path: '/teacher/CreateRoom',
        name: 'createRoom',
        component: CreateRoom
      },
      {
        path: '/teacher/livingRoom',
        component: TeacherLivingRoom
      },
    ],
  }
]

const router = new VueRouter({
  routes,
  mode: 'history',
})

export default router
