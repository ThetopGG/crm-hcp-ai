import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  hcps: [],
  selectedHCP: null,
  loading: false,
};

const hcpSlice = createSlice({
  name: "hcp",
  initialState,
  reducers: {
    setHCPs: (state, action) => {
      state.hcps = action.payload;
    },
    setSelectedHCP: (state, action) => {
      state.selectedHCP = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
  },
});

export const { setHCPs, setSelectedHCP, setLoading } = hcpSlice.actions;
export default hcpSlice.reducer;
