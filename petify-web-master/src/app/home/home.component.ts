import { Component, OnInit } from '@angular/core';
import { AdvertService } from '../services/advert.service';
import { TILES } from '../components/grid-view/grid-view.variables';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  adverts = [];
  loading = true;
  constructor(private advertService: AdvertService, private authService: AuthService) {
    this.advertService.getAdverts().then((rsp: any) => {
      this.authService.getDetails().then((info: any) => {
        rsp.reverse();
        let index = 0;
        rsp.forEach(advert => {
          if (info.user_id != advert.user_id) {
            advert.start_date = new Date(advert.start_date);
            advert.end_date = new Date(advert.end_date);
            this.adverts.push({ ...advert, tile: TILES[index] })
            index++;
            if (index == TILES.length) {
              index = 0;
            }
          }
        });
      }).catch((err) => {
        console.log(err);
      })
    }).catch((err) => {
      console.log(err);
    }).finally(() => {
      this.loading = false;
    })
  }
}
