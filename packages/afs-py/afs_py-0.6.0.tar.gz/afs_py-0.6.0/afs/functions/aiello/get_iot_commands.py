import afs
import contextvars
import typing
import httpx

DEVICE_UUID: contextvars.ContextVar[typing.Optional[typing.Text]] = contextvars.ContextVar("DEVICE_UUID", default=None)


async def get_iot_commands(request_model: "GetIotCommands") -> typing.Text:

"https://api-8b657.aiello.ai/api/v2/iot/{{device_uuid}}"

class GetIotCommands(afs.AfsBaseModel):
    device_uuid: typing.Text



"ac","ac","air conditioner","air conditioning","climate control","cooler","heater","temperature","thermostat","fans","airconditioner","aircon","air con","Accord","air condition","fan","aircon fan"
"air_exchange_fan","air exchange fan","ventilator","extractor fan","exhaust fan"
"bed","bed","mattress"
"blind","blind","blinds","day blind","day blinds","shutters"
"blockout_curtain","blockout_curtain","blockout curtain","blackout"
"curtain","curtain","shade","drape","curtains","window shade","window shades","drapes"
"roller_blind","roller blind","roller blinds"
"sheer_curtain","sheer curtain"
"shower_curtain","shower curtain"
"background_light","background light","backgroud lamp"
"bedside_light","bedside light","bedside lamp","berth light","berth lamp","bed light","bed lamp","light on the bed","lights on the bed","light on bed","lights on bed","light on the bedside","lights on the bedside","light on bedside","lights on bedside","headboard light"
"ceiling_light","ceiling light","ceiling lights","ceiling lamp","down light","recessed spotlights","recessed spotlight","down lights","downlights","downlight"
"desk_light","desk lamp","desk light","table lamp","table light","light on the desk","light on desk","lamp on the desk","lamp on desk","make-up lights"
"floor_lamp","floor lamp","floor light","standard lamp","standard light","floor lights","standard lights"
"indirect_light","indirect light","indirect lights","hidden light","hidden lights"
"light","lamp","light","lights","sconce","sconces","led lights","led light","lighting","lamps"
"night_light","nightlight","night light","night-light","night lamp","sleep light","sleeping light","sleep lamp","sleeping lamp","sleeping lights","sleep lights"
"pendant_light","pendant light","pendant lamp","pendant lights"
"reading_light","reading light","reading lamp","reading mode light","reading lights","reading lamps","read mode light"
"recessed_light","recessed light","recessed lights","downlight"
"track_light","track light","track lamp","track lights"
"wall_light","wall light","wall lamp","wall sconces","wall sconce"
"tv","TV","television","tv","TVs","Projector","projecter"
