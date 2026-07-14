import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  globalLoading: false,
  snackbar: { open: false, message: "", severity: "info" },
};

const uiSlice = createSlice({
  name: "ui",
  initialState,
  reducers: {
    setGlobalLoading: (state, action) => {
      state.globalLoading = action.payload;
    },
    showSnackbar: (state, action) => {
      state.snackbar = { open: true, message: action.payload.message, severity: action.payload.severity || "info" };
    },
    hideSnackbar: (state) => {
      state.snackbar.open = false;
    },
  },
});

export const { setGlobalLoading, showSnackbar, hideSnackbar } = uiSlice.actions;
export default uiSlice.reducer;
