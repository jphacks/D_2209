<template>
  <div>
   
   <div ref="map" style="height:550px;width:400px;"></div>
   <h1>Google Map</h1>
  </div>
  </template>
  
  <script>
  export default {
    data(){
      return {
        map:'',
      }
    },
    mounted(){
      let timer = setInterval(() => {
        if(window.google){
          clearInterval(timer);
          this.map = new window.google.maps.Map(this.$refs.map, {
            center: {lat: -34.397, lng: 150.644},
            zoom: 13
          });       
        }
      },500)
    }
  }
  </script>