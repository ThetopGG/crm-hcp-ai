import React from "react";
import { Box, Toolbar } from "@mui/material";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

export default function MainLayout({ children }) {
  return (
    <Box sx={{ display: "flex", minHeight: "100vh", backgroundColor: "background.default" }}>
      <Navbar />
      <Sidebar />
      <Box component="main" sx={{ flexGrow: 1, p: 3, ml: "0px" }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
}
