<script>
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  props: ['x', 'y', 'options', 'target'],
  mounted () {
    this.renderLineChart()
  },
  methods: {
    renderLineChart: function () {
      var dataset = [{
        label: 'Current',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderColor: 'rgba(255, 99, 132, 1)',
        data: this.y
      }]
      if (this.target) {
        dataset.push({
          label: 'Target',
          backgroundColor: 'rgba(255, 255, 26, 0.4)',
          borderColor: 'rgba(244, 158, 66, 1)',
          data: this.target,
          borderDash: [5, 5]
        })
      }
      if (this.options.previous === true) {
        dataset.push({
          label: 'Previous',
          backgroundColor: 'rgba(255, 0, 132, 0.4)',
          borderColor: 'rgba(255, 0, 132, 0.6)',
          data: []
        })
      }

      this.renderChart(
        {
          labels: this.x,
          datasets: dataset
        },
        { responsive: true,
          maintainAspectRatio: false,
          elements: { point: { radius: 0 } }
        }
      )
    }
  },
  watch: {
    y: function () {
      // this.$data._chart.destroy()
      // this.renderLineChart()
      var dataArray = this.$data._chart.data.datasets

      if (this.options.previous === true) {
        dataArray[dataArray.length - 1].data = this.$data._chart.data.datasets[0].data
      }
      dataArray[0].data = this.y
      this.$data._chart.update()
    },
    target: function () {
      var dataArray = this.$data._chart.data.datasets

      dataArray[1].data = this.target
      this.$data._chart.update()
    }
  }
}
</script>
