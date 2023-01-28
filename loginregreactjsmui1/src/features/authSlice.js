import { createSlice } from '@reduxjs/toolkit'
import { getToken } from '../services/LocalStorageService'

const initialState = {
  access_token: getToken().access_token,
}

export const authSlice = createSlice({
  name: 'auth_token',
  initialState,
  reducers: {
    setUserToken: (state, action) => {
      state.access_token = action.payload.access_token
    },
    unSetUserToken: (state, action) => {
      console.log(action,state)
      state.access_token = action.payload.access_token
    },
  },
})

export const { setUserToken, unSetUserToken } = authSlice.actions

export default authSlice.reducer