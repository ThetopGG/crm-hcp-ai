import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./slices/authSlice";
import chatReducer from "./slices/chatSlice";
import interactionReducer from "./slices/interactionSlice";
import hcpReducer from "./slices/hcpSlice";
import uiReducer from "./slices/uiSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    chat: chatReducer,
    interactions: interactionReducer,
    hcp: hcpReducer,
    ui: uiReducer,
  },
});
