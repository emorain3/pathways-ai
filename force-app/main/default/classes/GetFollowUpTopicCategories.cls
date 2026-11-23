public with sharing class GetFollowUpTopicCategories {

    public class Request {
        @InvocableVariable(
            label='Load Current Categories'
            description='Set true to retrieve current follow-up topic categories.'
            required=true
        )
        public Boolean loadCategories;
    }

    public class Response {
        @InvocableVariable(
            label='Topic Categories JSON'
            description='JSON array of active categories with label and value. Show label to the learner; use value when creating the request.'
        )
        public String topicOptionsJson;
    }

    public class TopicOption {
        public String label;
        public String value;
    }

    @InvocableMethod(
        label='Get Follow-Up Topic Categories'
        description='Read the current active follow-up topic categories from Salesforce metadata.'
    )
    public static List<Response> getCategories(List<Request> requests) {

        List<TopicOption> options = new List<TopicOption>();

        for (Schema.PicklistEntry entry :
            Follow_Up_Request__c.Topic_Category__c
                .getDescribe().getPicklistValues()) {

            if (entry.isActive()) {
                TopicOption option = new TopicOption();
                option.label = entry.getLabel();
                option.value = entry.getValue();
                options.add(option);
            }
        }

        String choicesJson = JSON.serialize(options);
        List<Response> responses = new List<Response>();

        for (Request request : requests) {
            Response response = new Response();
            response.topicOptionsJson =
                request.loadCategories == true ? choicesJson : '[]';
            responses.add(response);
        }

        return responses;
    }
}