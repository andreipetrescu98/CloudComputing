import { Component, OnInit, Input } from '@angular/core';
import { MediaObserver } from '@angular/flex-layout';
import { AuthService } from 'src/app/services/auth.service';
import { AdvertService } from 'src/app/services/advert.service';
import { MatDialog } from '@angular/material/dialog';
import { SeeMoreDialog } from 'src/app/dialogs/see-more/see-more.dialog';

@Component({
  selector: 'app-grid-view',
  templateUrl: './grid-view.component.html',
  styleUrls: ['./grid-view.component.scss']
})
export class GridViewComponent {
  cols = 1;
  @Input() adverts = [];
  @Input() canSubscribe;
  constructor(private media: MediaObserver, private authService: AuthService, private advertService: AdvertService, private dialog: MatDialog) { }

  ngAfterViewInit() {
    setTimeout(() => {
      // ObservableMedia does not fire on init so you have to manually update the grid first.
      this.updateGrid();
      this.media.media$.subscribe(change => { this.updateGrid(); });
    }, 100);
  }

  updateGrid(): void {
    if (this.media.isActive('xl')) { this.cols = 12; }
    else if (this.media.isActive('lg')) { this.cols = 10; }
    else if (this.media.isActive('md')) { this.cols = 2; }
    else if (this.media.isActive('sm')) { this.cols = 1; }
    else if (this.media.isActive('xs')) { this.cols = 1; }
  }

  getDetails(advert, index) {
    const dialogRef = this.dialog.open(SeeMoreDialog, {
      width: '70rem',
      maxWidth: '100vw',
      // height: '70vh',
      data: { 'advert': advert, canSubscribe: this.canSubscribe },
      panelClass: 'dialog-props',
    });
    dialogRef.afterClosed().subscribe(result => {
      if(result){
        this.subscribeToAdvert(advert, index)
      }
    });
  }

  subscribeToAdvert(advert, index) {
    this.authService.getDetails().then((info: any) => {
      this.advertService.subscribeToAdvert({ advert_id: advert.id, user_id: info.user_id }).then((rsp) => {
        this.adverts.splice(index, 1);
      }).catch((err) => {
        console.log(err);
      })
    }).catch((err) => {
      console.log(err);
    })
  }

}
