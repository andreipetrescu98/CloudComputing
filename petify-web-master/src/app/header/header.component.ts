import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { AddAdvertDialog } from '../dialogs/add-advert/add-advert.dialog';
import { MatDialog } from '@angular/material/dialog';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  @Output() onNavOpen: EventEmitter<any> = new EventEmitter();

  user = null;

  constructor(private dialog: MatDialog, private authService: AuthService) {
    this.authService.getDetails().then((rsp: any) => {
      this.user = {
        name: rsp.user_claims.filter(claim => claim.typ.includes("givenname"))[0].val,
        picture: rsp.user_claims.filter(claim => claim.typ.includes("picture"))[0].val,
        email: rsp.user_claims.filter(claim => claim.typ.includes("emailaddress"))[0].val
      }
    })
  }

  ngOnInit(): void {
  }

  openNav() {
    this.onNavOpen.emit('open');
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(AddAdvertDialog, {
      width: '70rem',
      maxWidth: '100vw',
      panelClass: 'dialog-props',
    });

    dialogRef.afterClosed().subscribe(result => {
    });
  }

  logout() {
    window.alert('logout!')

  }

}
