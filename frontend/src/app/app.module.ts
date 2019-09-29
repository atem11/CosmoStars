import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {
  MatAutocompleteModule, MatButtonModule,
  MatButtonToggleModule,
  MatCardModule,
  MatChipsModule, MatDividerModule,
  MatExpansionModule, MatFormFieldModule,
  MatGridListModule,
  MatIconModule, MatInputModule, MatListModule
} from '@angular/material';
import {HttpClientModule} from '@angular/common/http';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ReactiveFormsModule} from '@angular/forms';
import {SatDatepickerModule, SatNativeDateModule} from 'saturn-datepicker';
import { PostComponent } from './post/post.component';

@NgModule({
  declarations: [
    AppComponent,
    PostComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MatButtonModule,
    MatCardModule,
    MatChipsModule,
    MatExpansionModule,
    MatIconModule,
    MatFormFieldModule,
    MatAutocompleteModule,
    SatDatepickerModule,
    SatNativeDateModule,
    ReactiveFormsModule,
    MatInputModule,
    MatDividerModule,
    MatButtonToggleModule,
    MatListModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
