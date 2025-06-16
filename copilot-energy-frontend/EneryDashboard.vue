<template>
  <div>
    <h2>Real-Time Energy Data</h2>
    <apexchart type="line" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script>
import axios from "axios";
import VueApexCharts from "vue-apexcharts";

export default {
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: [{ name: "Voltaje A", data: [] }],
      chartOptions: {
        chart: { id: "energy-chart" },
        xaxis: { type: "datetime" },
      },
    };
  },
  mounted() {
    this.obtenerDatos();
    setInterval(this.obtenerDatos, 2000);
  },
  methods: {
    async obtenerDatos() {
      try {
        const response = await axios.get("https://copilot-energy-web.onrender.com/datos");
        const newData = response.data.map(item => ({ x: new Date(item.timestamp).getTime(), y: item.voltaje_A }));
        this.series[0].data = newData;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>
