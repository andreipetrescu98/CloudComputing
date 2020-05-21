import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from './auth.service';

@Injectable({
    providedIn: 'root'
})
export class ImageService {

    constructor(private http: HttpClient, private authService: AuthService) {

    }

    public uploadImage(imgObj) {
        return this.http.post("https://petify-api.azurewebsites.net/upload-image", imgObj).toPromise()
    }

}