<script>
import { Line } from 'vue-chartjs'
import linspace from 'linspace'

export default {
  extends: Line,
  props: ['y', 'y2', 'target', 'hasHistory'],
  mounted () {
    this.renderLineChart()
  },
  data: function () {
    return {
      time: linspace(0, 2 * Math.PI, 25000)
    }
  },
  methods: {
    renderLineChart: function () {
      var dataset = [{
        label: 'Current',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderColor: 'rgba(255, 99, 132, 1)',
        data: this.y_data
      }]

      if (this.target) {
        dataset.push({
          label: 'Target',
          backgroundColor: 'rgba(255, 255, 26, 0.4)',
          borderColor: 'rgba(244, 158, 66, 1)',
          data: this.target_data,
          borderDash: [5, 5]
        })
      }

      if (this.hasHistory === true) {
        dataset.push({
          label: 'Previous',
          borderColor: 'rgba(255, 0, 132, 0.6)',
          fill: false,
          borderDash: [5, 5],
          data: []
        })
      }

      this.renderChart(
        {
          labels: this.x_labels,
          datasets: dataset
        },
        { responsive: true,
          maintainAspectRatio: false,
          elements: { point: { radius: 0 } }
        }
      )
    }
  },
  computed: {
    y_data: function () {
      return this.time.map(t => this.y.amplitude * Math.sin(this.y.frequency * t))
    },
    y2_data: function () {
      if (this.y2) {
        return this.time.map(t => this.y2.amplitude * Math.sin(this.y2.frequency * t))
      } else {
        return this.time.map(t => 0)
      }
    },
    wave_data: function () {
      return this.time.map((t, idx) => this.y_data[idx] + this.y2_data[idx])
    },
    x_labels: function () {
      return this.time.map(x => Math.round(x * 100) / 100)
    },
    target_data: function () {
      if (this.target) {
        var y1 = this.time.map(t => this.target.wave1.amplitude * Math.sin(this.target.wave1.frequency * t))
        var y2 = this.time.map(t => this.target.wave2.amplitude * Math.sin(this.target.wave2.frequency * t))
        return this.time.map((t, idx) => y1[idx] + y2[idx])
      } else {
        return []
      }
    }
  },
  watch: {
    wave_data: function () {
      var dataArray = this.$data._chart.data.datasets

      if (this.hasHistory) {
        dataArray[dataArray.length - 1].data = this.$data._chart.data.datasets[0].data
      }
      dataArray[0].data = this.wave_data
      this.$data._chart.update()
    },
    target_data: function () {
      var dataArray = this.$data._chart.data.datasets

      dataArray[1].data = this.target_data
      this.$data._chart.update()
    }
  }
}
</script>
