<script>
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  props: ['x', 'y', 'options'],
  mounted () {
    this.renderLineChart()
  },
  methods: {
    renderLineChart: function () {
      var dataset = [{
        label: 'Current',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        data: this.y
      }]
      if (this.options.hasOwnProperty('target')) {
        dataset.push({
          label: 'Target',
          backgroundColor: 'rgba(255, 0, 132, 0.4)',
          data: this.options.target
        })
      }
      if (this.options.previous === true) {
        dataset.push({
          label: 'Previous',
          backgroundColor: 'rgba(255, 0, 132, 0.4)',
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
    }
  }
}
</script>
