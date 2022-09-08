import pytest
import operator
from graphql_relay import to_global_id

pytestmark = pytest.mark.django_db


class TestAllNotificationsQuery:
    QUERY = '''
        query  {
          allNotifications {
            edges {
              node {
                id
                type
                data
              }
            }
          }
        }
    '''

    def test_returns_empty_list(self, graphene_client, user):
        graphene_client.force_authenticate(user)
        executed = graphene_client.query(self.QUERY)

        assert executed == {'data': {'allNotifications': {'edges': []}}}

    def test_returns_all_notifications_sorted_by_created_at(self, graphene_client, user, notification_factory):
        graphene_client.force_authenticate(user)
        notifications = notification_factory.create_batch(3, user=user)
        executed = graphene_client.query(self.QUERY)

        assert executed == {
            'data': {
                'allNotifications': {
                    'edges': [
                        {
                            'node': {
                                'id': to_global_id('NotificationType', str(notification.id)),
                                'type': notification.type,
                                'data': notification.data,
                            }
                        }
                        for notification in sorted(notifications, key=operator.attrgetter('created_at'), reverse=True)
                    ]
                }
            }
        }

    def test_returns_only_notifications_that_belong_to_logged_in_user(
        self, graphene_client, user_factory, notification_factory
    ):
        user = user_factory()
        other_user = user_factory()
        graphene_client.force_authenticate(user)
        notification = notification_factory(user=user)
        notification_factory(user=other_user)
        executed = graphene_client.query(self.QUERY)

        assert executed == {
            'data': {
                'allNotifications': {
                    'edges': [
                        {
                            'node': {
                                'id': to_global_id('NotificationType', str(notification.id)),
                                'type': notification.type,
                                'data': notification.data,
                            }
                        }
                    ]
                }
            }
        }
