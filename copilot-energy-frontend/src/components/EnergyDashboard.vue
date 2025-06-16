<template>
  <div>
    <h2>Real-Time Energy Data</h2>
    <VueApexChart type="line" :options="chartOptions" :series="series"></VueApexChart>
  </div>
</template>

<script>
import axios from "axios";
import VueApexCharts from "vue3-apexcharts"; // ✅ Ensure it's correctly imported

export default {
  components: {
    VueApexChart: VueApexCharts, // ✅ Register VueApexChart properly
  },
  data() {
    return {
      series: [{ name: "Voltaje A", data: [] }],
      chartOptions: {
        chart: {
          id: "energy-chart",
          animations: { enabled: true }, // ✅ Enable chart animations
        },
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
      console.log("Received Data:", response.data); // ✅ Debugging
      
      if (response.data.length > 0) {
        this.series[0].data.push({ // ✅ Append new data instead of replacing
          x: new Date(response.data[0].timestamp).getTime(),
          y: response.data[0].voltaje_A,
        });
      } else {
        console.warn("No data received from backend.");
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  },
}
,
};
</script>
