import { Component, Inject, ViewChild } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogData } from './add-advert.data';
import { AuthService } from 'src/app/services/auth.service';
import { ImageService } from 'src/app/services/image.service';
import { AdvertService } from 'src/app/services/advert.service';

class ImageSnippet {
    pending: boolean = false;
    status: string = 'init';

    constructor(public src: string, public file: File) {
    }
}

@Component({
    selector: 'add-advert-dialog',
    templateUrl: 'add-advert.html',
    styleUrls: ['./add-advert.dialog.scss']
})
export class AddAdvertDialog {
    key: string = '0if5RUt72eN4jFibG1uMTC_-GJ0a3rDIJBTerd3FVR8'
    selectedFile: ImageSnippet;
    data: DialogData = {
        title: null,
        description: null,
        price: null,
        start_date: null,
        end_date: null,
        location: null,
        image: null,
        availability: null,
        user_id: null,
        user_name: null,
        user_picture: null
    };
    public config = {
        'zoom': 1.5,
        'center': [20, 20],
        'interactive': true,
    };
    load = 'map';


    constructor(
        public dialogRef: MatDialogRef<AddAdvertDialog>,
        private authService: AuthService,
        private imageService: ImageService,
        private advertService: AdvertService) {
        this.authService.getDetails().then((rsp: any) => {
            this.data.user_name = rsp.user_claims.filter(claim => claim.typ == "name")[0].val;
            this.data.user_picture = rsp.user_claims.filter(claim => claim.typ.includes("picture"))[0].val;
            this.data.user_id = rsp.user_id;
        })
    }

    ngOnInit() {
        setTimeout(() => {
            if (!this.data.location) {
                this.data.location = "0,0";
                this.load = null;
            }
        }, 10000);
    }

    onNoClick(): void {
        this.dialogRef.close();
    }

    processFile(image) {
        const file: File = image.files[0];
        const reader = new FileReader();

        reader.addEventListener('load', (event: any) => {
            this.selectedFile = new ImageSnippet(event.target.result, file);
        });

        reader.readAsDataURL(file);
    }

    updateLocation(coords) {
        this.load = null;
        this.data.location = coords.join(',');
    }

    addAdvert() {
        let dto = { ...this.data };
        dto.start_date = (dto.start_date as any).toISOString();
        dto.end_date = (dto.end_date as any).toISOString();
        this.load = 'advert';
        this.advertService.addAdvert(dto).then((rsp: any) => {
            this.load = 'image';
            if (this.selectedFile) {
                this.imageService.uploadImage({
                    advertId: rsp.advert_id,
                    imageData: this.selectedFile.src.split('base64,')[1]
                }).then((rsp) => {
                    this.dialogRef.close();
                }).catch((err) => {
                    console.log(err);
                    this.dialogRef.close();
                })
            }
        }).catch((err) => {
            console.log(err);
            this.dialogRef.close();
        })
    }

}