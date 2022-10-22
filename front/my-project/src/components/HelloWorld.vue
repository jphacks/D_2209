<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    
  </div>
  
</template>

<script>

import TabMenu from '@/components/TabMenu'

export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: '地図をなぞって、雰囲気検索。'
    }
  },
  
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-family: 'Yusei Magic', sans-serif;
  font-weight: bold;
  text-align: left;
  margin-left:20px;
  font-size: 18px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
