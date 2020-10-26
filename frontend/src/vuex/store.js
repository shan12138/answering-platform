import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    account: sessionStorage.getItem('username'),
    //身份代码
    user_id: sessionStorage.getItem('user_id'),
    //0代表管理员 1代表老师 2代表学生
    identity: 2,
    // 当前所在房间的id
    room_id: sessionStorage.getItem('room_id'),
    // 学生是否认证
    is_verify: false,  
    // 学生是否被禁言  true 被禁言 ， false未有
    user_state: false,

    appId: '498f87ed8b6f4220947ea1e29d5507cb'
  },

  getter : {
    getUserId(state) {
      return state.user_id
    }
  },
  actions: {
    setRoomIdInfo({commit}, roomid) {
      commit('setRoomID', roomid)
    },

    serUserIdInfo({commit}, user_id) {
      commit('setUserId', user_id)
    },
    setUserAccountInfo({commit}, account) {
      commit('setAccount', account)
    },
    setIsVarifyInfo({commit}, is_verify) {
      commit('setIsVerify', is_verify)
    },
    setUserStateInfo({commit}, user_state) {
      commit('setUserState', user_state)
    }

    
  },
  mutations: {
    setUserId(state, userid) {
      state.user_id = userid
    },
    setAccount(state, account) {
      state.account = account
    },
    setRoomID(state, room_id) {
      state.room_id = room_id
    },
    setVarify(state, is_verify) {
      state.is_verify = is_verify
    },
    setUserState(state, user_state) {
      state.user_state = user_state
    }
  }
})

export default store