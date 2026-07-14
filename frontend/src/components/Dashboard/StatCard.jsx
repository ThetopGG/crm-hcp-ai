import React from "react";
import { Card, CardContent, Box, Typography, Avatar } from "@mui/material";

export default function StatCard({ label, value, icon, color = "primary.main" }) {
  return (
    <Card sx={{ height: "100%" }}>
      <CardContent sx={{ display: "flex", alignItems: "center", gap: 2 }}>
        <Avatar sx={{ bgcolor: color, width: 48, height: 48 }}>{icon}</Avatar>
        <Box>
          <Typography variant="h5" fontWeight={700}>
            {value}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {label}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}
