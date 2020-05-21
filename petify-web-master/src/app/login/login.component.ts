import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginRef;
  constructor() {
    this.loginRef = `https://petify-api.azurewebsites.net/.auth/login/google?post_login_redirect_uri=${window.origin}&redirect_uri=${window.origin}`;
  }

  ngOnInit(): void {
  }

}
