<template>
  <div class="output">
    <h1>{{ msg }}</h1>
    <div v-for="(item, index) in items" :key=index>
    <div ref="map" style="height:300px;width:300px;"></div>
   </div>
  </div>
</template>

<script>
export default {
  name: 'Output',
  data () {
    return {
      msg: '検索結果：'+Object.keys(data[items]).length+'件のエリア',
      map:undefined,

      items: [{"lat": 36.285451, "lng": 139.33457}, {"lat": 34.696549, "lng": 137.946496}, {"lat": 36.269451, "lng": 139.16457}, {"lat": 34.713996, "lng": 136.486291}, {"lat": 36.109776, "lng": 140.218836}, {"lat": 35.861776, "lng": 140.338836}, {"lat": 36.085451, "lng": 139.76457}, {"lat": 36.093451, "lng": 139.42457}, {"lat": 36.085776, "lng": 140.218836}, {"lat": 36.018263, "lng": 139.98638}]

      /*name: 'カメラアプリを作成した',
      text: 'このような意図で作成しました。ここをこのように工夫しました。ここが難しかったです。今後はこうゆう機能を追加したいです。'.repeat(3)*/

    }
  },
  mounted(){

const map = new window.google.maps.Map(this.$refs.map, {
   center: {lat: 100, lng: 100},
   zoom: 13,
   streetViewControl:false, // ストリートビュー非表示
   fullscreenControl:false // フルスクリーン非表示
 });  
 this.map = map;
}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

div.output {
  text-align: center;
}

div.content {
  background-color: #eee;
  display: inline-block;
  margin: 10px;
  width: 30%;
}

h3 {
  color: white;
}

h1, h2 {
  font-family: 'Yusei Magic', sans-serif;
  font-weight: bold;
  text-align: left;
  margin-left:20px;
  font-size: 18px;
}

p {
  width: 90%;
  display: inline-block;
  text-align: left;
}

</style>