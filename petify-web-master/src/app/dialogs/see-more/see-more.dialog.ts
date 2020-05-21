import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { AdvertService } from 'src/app/services/advert.service';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-see-more',
  templateUrl: './see-more.component.html',
  styleUrls: ['./see-more.component.scss']
})
export class SeeMoreDialog implements OnInit {
  uid;
  advertLocation;
  advert;
  canSubscribe;
  constructor(
    public dialogRef: MatDialogRef<SeeMoreDialog>,
    private authService: AuthService,
    private advertService: AdvertService,
    @Inject(MAT_DIALOG_DATA) public data: any) {
    this.authService.getDetails().then((rsp: any) => {
      this.uid = rsp.user_id;
    })
    this.advert = data.advert;
    this.canSubscribe = data.canSubscribe;
    let [lng, lat] = this.advert.location.split(',');
    this.advertLocation = {
      lng: parseFloat(lng),
      lat: parseFloat(lat)
    }

  }

  ngOnInit(): void {

  }

  close() {
    this.dialogRef.close(false);
  }

  subscribe() {
    this.dialogRef.close(true);
  }
}
