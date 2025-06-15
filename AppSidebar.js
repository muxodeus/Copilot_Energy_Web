import React from "react";
import { Sidebar, Menu, MenuItem, Submenu, Logo } from "react-mui-sidebar";

const AppSidebar = () => {
  return (
    <Sidebar width={"270px"}>
      <Logo img="https://adminmart.com/wp-content/uploads/2024/03/logo-admin-mart-news.png">
        Analítica Energética
      </Logo>

      <Menu subHeading="INICIO">
        <MenuItem link="/">Dashboard General</MenuItem>
      </Menu>

      <Menu subHeading="TIEMPO REAL">
        <MenuItem link="/tiempo-real">Monitoreo en Vivo</MenuItem>
      </Menu>

      <Menu subHeading="HISTÓRICOS">
        <Submenu title="Análisis">
          <MenuItem link="/tendencias">Tendencias</MenuItem>
          <MenuItem link="/estadisticas">Estadísticas</MenuItem>
          <MenuItem link="/factor-carga">Factor de Carga</MenuItem>
        </Submenu>
      </Menu>

      <Menu subHeading="REPORTES">
        <MenuItem link="/iec-61000-4-30">Norma IEC 61000-4-30</MenuItem>
        <MenuItem link="/otros-reportes">Otros Reportes</MenuItem>
      </Menu>

      <Menu subHeading="CUENTA">
        <MenuItem link="/perfil">Perfil de Usuario</MenuItem>
        <MenuItem link="/accesos">Accesos y Configuración</MenuItem>
      </Menu>
    </Sidebar>
  );
};

export default AppSidebar;
