const state = {
    selectedDate: new Date().toISOString().split('T')[0] // 默认设置为今天
}

const mutations = {
    setSelectedDate(state, date) {
        state.selectedDate = date
    }
}

const actions = {
    updateSelectedDate({ commit }, date) {
        commit('setSelectedDate', date)
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
} 