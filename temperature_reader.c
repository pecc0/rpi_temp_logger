#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <syslog.h>

#define MAXTIMINGS	85
#define DHTPIN		7
int dht11_dat[5] = { 0, 0, 0, 0, 0 };
 
int read_dht11_dat(float* temperature, float* humidity)
{
	uint8_t laststate	= HIGH;
	uint8_t counter		= 0;
	uint8_t j		= 0, i;
	float	f; 
 
	dht11_dat[0] = dht11_dat[1] = dht11_dat[2] = dht11_dat[3] = dht11_dat[4] = 0;
 
	pinMode( DHTPIN, OUTPUT );
	digitalWrite( DHTPIN, LOW );
	delay( 18 );
	digitalWrite( DHTPIN, HIGH );
	delayMicroseconds( 40 );
	pinMode( DHTPIN, INPUT );
 
	for ( i = 0; i < MAXTIMINGS; i++ )
	{
		counter = 0;
		while ( digitalRead( DHTPIN ) == laststate )
		{
			counter++;
			delayMicroseconds( 1 );
			if ( counter == 255 )
			{
				break;
			}
		}
		laststate = digitalRead( DHTPIN );
 
		if ( counter == 255 )
			break;
 
		if ( (i >= 4) && (i % 2 == 0) )
		{
			dht11_dat[j / 8] <<= 1;
			if ( counter > 16 )
				dht11_dat[j / 8] |= 1;
			j++;
		}
	}
 
	if ( (j >= 40) &&
		(dht11_dat[4] == ( (dht11_dat[0] + dht11_dat[1] + dht11_dat[2] + dht11_dat[3]) & 0xFF) ) )
	{
		f = dht11_dat[2] * 9. / 5. + 32;
		syslog(LOG_INFO, "Humidity = %d.%d %% Temperature = %d.%d C (%.1f F)",
			dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3], f );
			
		//printf( "Humidity = %d.%d %% Temperature = %d.%d C (%.1f F)\n",
		//	dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3], f );
		if (dht11_dat[2] > 100)
		{
			return 0;
		}
		*temperature = dht11_dat[2];
		*humidity = dht11_dat[0];
		return 1;
	}else  {
		//syslog(LOG_INFO, "Data not good, skip" );
		return 0;
	}
}
 
int main( void )
{
	openlog("termometer", LOG_PID|LOG_CONS, LOG_USER);
	
	//syslog(LOG_INFO, "Termometer start" );
 
	if ( wiringPiSetup() == -1 )
		exit( 1 );
 
	while ( 1 )
	{
		float temperature;
		float humidity;
		if (read_dht11_dat(&temperature, &humidity))
		{
			printf("%.1f;%.1f", temperature, humidity);
			break;
		}
		delay( 1000 ); 
	}
 
	closelog();
	
	return(0);
}