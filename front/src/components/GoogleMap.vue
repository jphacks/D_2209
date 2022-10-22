<template>
  <div id="app" class="mt-4">
   
   <div ref="map" style="height:550px;width:400px;"></div>
   <h1>Google Map</h1>
   {{position}}
  
  </div>
  </template>
  
  <script>
  export default {
    name: 'App',
    data(){
      return {
        map:undefined,
        position:undefined,
        bounds:undefined,
        path:[],
        line:undefined
      }
    },

    methods:{
      clickOnMap(mapEvent){
      console.log(mapEvent.latLng.toString())
      this.position = mapEvent.latLng.toString();
      },

      drawLine(mapEvent){
        let latLng = mapEvent.latLng;

         // １点目をクリック
        if(this.line === undefined){

          const newLine = new window.google.maps.Polyline({
            path:[latLng],
            geodesic: true,
            strokeColor: "#FF0000",
            strokeOpacity: 1.0,
            strokeWeight: 6,
          })

          newLine.setMap(this.map);
          this.path.push(latLng);
          this.line = newLine;
          return;
        }

       // ２点目以降
       this.path.push(latLng);
       this.line.setPath([...this.path]);
       //return{
        //path:this.path
       //};
      }
    },

    //リスナーの登録
    

    mounted(){

     const map = new window.google.maps.Map(this.$refs.map, {
        center: {lat: 34.5841973, lng: 135.5756114},
        zoom: 13,
        streetViewControl:false, // ストリートビュー非表示
        fullscreenControl:false // フルスクリーン非表示
      });       
        
      map.addListener('click',(mapsMouseEvent)=>{
        return this.clickOnMap(mapsMouseEvent);
      });

      map.addListener('click',(mapsMouseEvent)=>{
        return this.drawLine(mapsMouseEvent);
      });

      /*
      new window.google.maps.Polyline({
       path:[
        { lat: 34.855273888888888, lng: 135.30649 },
        { lat: 34.854465, lng: 135.8 },
      ],
      geodesic: true,
      strokeColor: "#FF0000",
      strokeOpacity: 1.0,
      strokeWeight: 2,
      }).setMap(map);
      */
      this.map = map;
      
    }
  }
  </script>