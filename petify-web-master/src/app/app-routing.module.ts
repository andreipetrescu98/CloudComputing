import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { MySubscriptionsComponent } from './my-subscriptions/my-subscriptions.component';
import { MyAdvertsComponent } from './my-adverts/my-adverts.component';
import { AdvertPageComponent } from './advert-page/advert-page.component';
import { AuthGuard } from './guards/auth.guard';


const routes: Routes = [
  {
    path: 'home', component: HomeComponent,
  },
  {
    path: 'subscriptions', component: MySubscriptionsComponent,
  },
  {
    path: 'adverts', component: MyAdvertsComponent,
  },
  {
    path: 'advert/:advertId', component: AdvertPageComponent,
  },
  { path: '', redirectTo: '/home', pathMatch: 'full' }, // redirect to `first-component`
  { path: '**', component: HomeComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
