<template>
  <div class="output">
    <div class="content" v-for="i in 6" :key=i>
    <h3> {{ name }} </h3>
    <p> {{ text }} </p>
  </div>
  </div>
</template>

<script>
export default {
  name: 'Output',
  data () {
    return {
      name: 'カメラアプリを作成した',
      text: 'このような意図で作成しました。ここをこのように工夫しました。ここが難しかったです。今後はこうゆう機能を追加したいです。'.repeat(3)
    }
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

p {
  width: 90%;
  display: inline-block;
  text-align: left;
}

</style>