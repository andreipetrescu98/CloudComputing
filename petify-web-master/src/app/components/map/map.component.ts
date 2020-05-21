import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged } from "rxjs/internal/operators";

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {
  map;
  datasource;
  client;
  searchInputLength;
  centerMapOnResults;



  //angular impl
  @Input() viewOnly;
  @Output() currPointChanged = new EventEmitter();
  searchModelChanged: Subject<string> = new Subject<string>();
  searchModel = '';
  results = [];
  currPoint;
  position;

  //The minimum number of characters needed in the search input before a search is performed.
  minSearchInputLength = 3;
  //The number of ms between key strokes to wait before performing a search.
  keyStrokeDelay = 150;


  constructor() {
    this.searchModelChanged.pipe(debounceTime(this.keyStrokeDelay), distinctUntilChanged()).subscribe(model => {
      this.searchModel = model;
      this.searchInputKeyup();
    });
  }

  ngOnInit(): void {
    if (this.viewOnly) {
      this.getMapViewOnly();
    } else {
      this.getMap();
    }
  }

  onSearchChange(query: string) {
    this.searchModelChanged.next(query);
  }

  searchInputKeyup = () => {
    this.centerMapOnResults = false;
    if (this.searchModel.length >= this.minSearchInputLength) {
      this.centerMapOnResults = true;
      this.search(this.searchModel);
    } else {
      this.results = [];
      this.datasource.clear();
      this.currPoint.setCoordinates(this.position);
      this.datasource.add([this.currPoint]);
    }
    this.searchInputLength = this.searchModel.length;
  }

  itemClicked(item) {
    let shape = this.datasource.getShapeById(item.id);
    this.map.setCamera({
      center: shape.getCoordinates(),
      zoom: 17
    });
    this.results = [];
    this.searchModel = item.properties.poi.name || item.properties.address.freeformAddress;
  }

  getMapViewOnly() {
    // debugger
    //Initialize a map instance.
    this.map = new window['atlas'].Map('myMap', {
      center: [this.viewOnly.lng, this.viewOnly.lat],
      zoom: 14,
      view: 'Auto',

      //Add your Azure Maps subscription key to the map SDK. Get an Azure Maps key at https://azure.com/maps
      authOptions: {
        authType: 'subscriptionKey',
        subscriptionKey: '0if5RUt72eN4jFibG1uMTC_-GJ0a3rDIJBTerd3FVR8'
      }
    });

    //Wait until the map resources are ready.
    this.map.events.add('ready', () => {

      //Add the zoom control to the map.
      this.map.controls.add(new window['atlas'].control.ZoomControl(), {
        position: 'top-right'
      });

      //Create a data source and add it to the map.
      this.datasource = new window['atlas'].source.DataSource();
      this.map.sources.add(this.datasource);

      this.currPoint = new window['atlas'].Shape(new window['atlas'].data.Point([this.viewOnly.lng, this.viewOnly.lat]));
      //Add the symbol to the data source.
      this.datasource.add([this.currPoint]);

      //Create a symbol layer using the data source and add it to the map
      this.map.layers.add(new window['atlas'].layer.SymbolLayer(this.datasource, null));
    });
  }

  getMap() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        this.position = position;
        const lng = position.coords.longitude;
        const lat = position.coords.latitude;
        //Initialize a map instance.
        this.map = new window['atlas'].Map('myMap', {
          center: [lng, lat],
          zoom: 14,
          view: 'Auto',

          //Add your Azure Maps subscription key to the map SDK. Get an Azure Maps key at https://azure.com/maps
          authOptions: {
            authType: 'subscriptionKey',
            subscriptionKey: '0if5RUt72eN4jFibG1uMTC_-GJ0a3rDIJBTerd3FVR8'
          }
        });

        //Wait until the map resources are ready.
        this.map.events.add('ready', () => {

          //Add the zoom control to the map.
          this.map.controls.add(new window['atlas'].control.ZoomControl(), {
            position: 'top-right'
          });

          //Create a data source and add it to the map.
          this.datasource = new window['atlas'].source.DataSource();
          this.map.sources.add(this.datasource);

          this.currPoint = new window['atlas'].Shape(new window['atlas'].data.Point([lng, lat]));
          this.currPointChanged.emit([lng, lat]);
          //Add the symbol to the data source.
          this.datasource.add([this.currPoint]);

          /* Gets co-ordinates of clicked location*/
          this.map.events.add('click', (e) => {
            /* Update the position of the point feature to where the user clicked on the map. */
            this.currPoint.setCoordinates(e.position);
            this.position = e.position;
            this.currPointChanged.emit(e.position);
          });

          //Create a symbol layer using the data source and add it to the map
          this.map.layers.add(new window['atlas'].layer.SymbolLayer(this.datasource, null));
        });
      });
    }
  }

  search(query) {
    //Remove any previous results from the map.
    this.datasource.clear();

    //Use SubscriptionKeyCredential with a subscription key
    let subscriptionKeyCredential = new window['atlas'].service.SubscriptionKeyCredential(window['atlas'].getSubscriptionKey());

    //Use subscriptionKeyCredential to create a pipeline
    let pipeline = window['atlas'].service.MapsURL.newPipeline(subscriptionKeyCredential);

    //Construct the SearchURL object
    let searchURL = new window['atlas'].service.SearchURL(pipeline);

    searchURL.searchPOI(window['atlas'].service.Aborter.timeout(10000), query, {
      lon: this.map.getCamera().center[0],
      lat: this.map.getCamera().center[1],
      maxFuzzyLevel: 4,
      view: 'Auto'
    }).then((results) => {

      //Extract GeoJSON feature collection from the response and add it to the datasource
      let data = results.geojson.getFeatures();
      this.datasource.add(data);

      if (this.centerMapOnResults) {
        this.map.setCamera({
          bounds: data.bbox
        });
      }
      this.results = data.features;
    });
  }
}
