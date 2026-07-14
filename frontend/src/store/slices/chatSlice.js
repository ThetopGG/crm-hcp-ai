import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  messages: [
    {
      role: "assistant",
      content:
        "Hi! Tell me about a meeting or call you'd like to log — e.g. \"I met Dr Sharma today at Apollo Hospital, we discussed CardX, he wants efficacy data next Monday.\"",
    },
  ],
  isSending: false,
  lastExtractedForm: null,
};

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    addUserMessage: (state, action) => {
      state.messages.push({ role: "user", content: action.payload });
    },
    addAssistantMessage: (state, action) => {
      state.messages.push({ role: "assistant", content: action.payload });
    },
    setSending: (state, action) => {
      state.isSending = action.payload;
    },
    setExtractedForm: (state, action) => {
      state.lastExtractedForm = action.payload;
    },
    resetChat: (state) => {
      state.messages = initialState.messages;
      state.lastExtractedForm = null;
    },
  },
});

export const { addUserMessage, addAssistantMessage, setSending, setExtractedForm, resetChat } = chatSlice.actions;
export default chatSlice.reducer;
