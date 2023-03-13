from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode , Decimal
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import decimal
from wsgiref.simple_server import make_server

# Le service va dire autant que fois qu'on le demande notre nom
class CalculTrajetService(ServiceBase):
    @rpc(Integer, Integer, Integer, Integer, _returns=Integer)
    def tempsTrajet(ctx, distanceEnKm, vMoyKmH, tempsArretMin, autonomieEnKm):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'
        nbArret = int(distanceEnKm / autonomieEnKm)
        tempsTotalAret = nbArret * tempsArretMin
        return tempsTotalAret + (distanceEnKm / vMoyKmH * 60)

application = Application([CalculTrajetService], 'spyne.examples.trajet.soap',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11())
wsgi_application = WsgiApplication(application)


server = make_server('127.0.0.1', 8000, wsgi_application)
server.serve_forever()