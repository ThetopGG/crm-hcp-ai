import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  interactions: [],
  currentInteraction: null,
  loading: false,
};

const interactionSlice = createSlice({
  name: "interactions",
  initialState,
  reducers: {
    setInteractions: (state, action) => {
      state.interactions = action.payload;
    },
    addInteraction: (state, action) => {
      state.interactions.unshift(action.payload);
    },
    setCurrentInteraction: (state, action) => {
      state.currentInteraction = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
  },
});

export const { setInteractions, addInteraction, setCurrentInteraction, setLoading } = interactionSlice.actions;
export default interactionSlice.reducer;
