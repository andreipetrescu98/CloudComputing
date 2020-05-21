import { Component, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Petify';
  @ViewChild('sidenav') sidenav: MatSidenav;

  constructor() {

  }

  ngOnInit() {
  }

  close(reason: string) {
    this.sidenav.close();
  }
}
